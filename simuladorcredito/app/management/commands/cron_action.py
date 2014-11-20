#https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
#python manage.py my_cool_command
from django.core.management.base import BaseCommand, CommandError
from app.models import PaymentPlan
import time
from random import randint
from threading import Thread
from app.utils import process_queue

def cpu_waste():
	target_time = time.clock() + 25
	while time.clock() < target_time:
                #Usa 85%+ de un core y un 25% en promedio de la cpu
                randint(2,9) % randint(2,9)
                pass
        


class Command(BaseCommand):
    help = 'Cambia el estado de todas los planes de pago a cerrado'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
    	payment_plans = PaymentPlan.objects.filter(state=False)[:1]
        cpu_waste()
        for plan in payment_plans:
        	#Hace cada una de las operaciones intensivas en un thread aparte, esto da 
        	#un total de 25 segundos por todos los planes. Si no se quiere este resultado 
        	#quitar el thread y dejar el llamado al metodo solo
        	#cpu_waste()
        	#thread = Thread(target = cpu_waste)
        	#thread.start()
            plan.state = True
            plan.save()
            process_queue("payment_plans_queue", plan.risk_indicator)
            self.stdout.write('Successfully closed plan "%s"' % plan)
        #thread.join()

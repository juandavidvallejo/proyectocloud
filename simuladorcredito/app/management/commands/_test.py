import time
from random import randint
from threading import Thread

def cpu_waste():
        target_time = time.clock() + 25
        while time.clock() < target_time:
                #Usa 85%+ de un core y un 25% en promedio de la cpu
                randint(2,9) % randint(2,9)
                pass

if __name__ == "__main__":
        for i in range(1,100):
                thread = Thread(target = cpu_waste)
                thread.start()
        thread.join()

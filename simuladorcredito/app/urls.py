from django.conf.urls import patterns, include, url
from views import index, signup, user_login, user_logout, public, public_plan, private, private_plan, create_credit_line, update_credit_line, delete_credit_line

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index, name='index'),
    url(r'^signup/', signup, name='signup'),
    url(r'^login/', user_login, name='user_login'),
    url(r'^logout/', user_logout, name='user_logout'),
    #Crea una nueva linea de credito
    url(r'^credit_line/create/$', create_credit_line, name='create_credit_line'),
    #Le hace update a una linea de credito creada (update)
    url(r'^credit_line/(?P<credit_line_id>[-\w]+)/update/$', update_credit_line, name='update_credit_line'),
    #Le hace update a una linea de credito creada (delete)
    url(r'^credit_line/(?P<credit_line_id>[-\w]+)/delete/$', delete_credit_line, name='delete_credit_line'),
    #Muestra todos las lineas de pago de una pyme
    url(r'^public/(?P<pyme_id>[-\w]+)/$', public, name='public'),
    #Muestra el template de creacion de un plan de pago con una linea de credito especifica
    url(r'^public/(?P<pyme_id>[-\w]+)/(?P<plan_id>[-\w]+)/$', public_plan, name='public_plan'),
    #Muestra la lista de todos los planes de pago de un administrador
	url(r'^private/$', private, name='private'),
	#Muestra un plan de pagos especifico
    url(r'^private/(?P<plan_id>[-\w]+)/$', private_plan, name='private_plan'),
)

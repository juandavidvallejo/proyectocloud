# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import uuid
from django.template.defaultfilters import slugify
from random import uniform
from django.core.validators import MaxValueValidator, MinValueValidator

def make_uuid():
    return str(uuid.uuid1().int>>64)

#El usuario cuando se crea genera un slug unico que es el que le manda a los clientes. 
#Cuando estos entran, salen los links a las distintas lineas de credito url.com/app/slug_user/slug_credit_line
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile_field")
    #some common fields here, which are shared among both corporate and individual profiles
    user_name = models.CharField(_('Nombre'),max_length=100, help_text=_("Mi nombre"))
    last_name = models.CharField(_('Apellidos'),max_length=100, help_text=_("Mis apellidos"))
    email = models.EmailField(max_length=100, unique=True, help_text=_("Mi correo electronico"))
    slug = models.SlugField(unique=True, db_index=True, default="dummy")

    def save(self, *args, **kwargs):
    	if self.pk is None:
        	self.slug = slugify(make_uuid())
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.email

class CreditLine(models.Model):
    owner = models.ForeignKey(UserProfile, related_name="credit_line_owner")
    slug = models.SlugField(unique=True, db_index=True, default="dummy")
    credit_line_name = models.CharField(_('Nombre de la linea de credito'),max_length=100, help_text=_("El nombre de la nueva linea de credito"))
    interest_rate = models.FloatField(_('Tasa de interes'), help_text=_("La tasa de interes de la nueva linea de credito. El valor debe estar entre 0 y 100"), validators = [MinValueValidator(0.1), MaxValueValidator(100.0)])

    def save(self, *args, **kwargs):
    	if self.pk is None:
        	self.slug = slugify(make_uuid())
        super(CreditLine, self).save(*args, **kwargs)

	def __str__(self):              # __unicode__ on Python 2
		return self.slug

class PaymentPlan(models.Model):
	owner = models.ForeignKey(UserProfile, related_name="payment_plan_owner")
	credit_line = models.ForeignKey(CreditLine, related_name="payment_plan_credit_line")
	identification_number = models.CharField(_('Cedula'), max_length=20, help_text=_("Mi cedula"))
	birth_date = models.DateField(_('Fecha Nacimiento'), help_text=_("Mi fecha de nacimiento"))
	duration_months = models.PositiveSmallIntegerField(_('Duracion en meses'), help_text=_("Duracion credito en meses"))
	principal = models.FloatField(_('Valor prestamo'), help_text=_("El valor del prestamo en pesos"))
	state = models.BooleanField(_('Estado'), default=False, help_text=_("Opciones: En Proceso (False) y  Generado (True)"))
	generation_date = models.DateField(auto_now_add=True, editable=False)
	risk_indicator = models.FloatField(_('Indicador del riesgo'), blank=True, default=-1.0, null=True, help_text=_("El indicador de riesgo"))
	slug = models.SlugField(unique=True, db_index=True, default="dummy")

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.slug = slugify(make_uuid())
		else:
			if self.state is True and self.risk_indicator is not -1:
				self.risk_indicator = uniform(0.0, 10.0)
		super(PaymentPlan, self).save(*args, **kwargs)

	def __str__(self):              # __unicode__ on Python 2
		return self.slug
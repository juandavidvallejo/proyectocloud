'''
Created on 3/07/2014

@author: usuario
'''
from django.forms import ModelForm, ValidationError, CharField, PasswordInput, HiddenInput, Form
from models import UserProfile, CreditLine, PaymentPlan
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class BaseUserForm(ModelForm):
    password = CharField(widget=PasswordInput(attrs={'class': 'input_text'}), label='Password')

    class Meta:
        model = User
        fields = ['username',]
        
        
    def save(self, commit=True):
        user = super(BaseUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserForm(ModelForm):
    #password = CharField(widget=PasswordInput(attrs={'class': 'input_text'}), label='Password')

    class Meta:
        model = UserProfile
        #fields = ['email', 'password']
        exclude = ('user', 'slug',)

    #===========================================================================
    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].required = True
    #===========================================================================

    #===========================================================================
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if UserProfile.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
    #         raise ValidationError(_(u'Email is already in use.'))
    #     return email
    #===========================================================================


class LoginForm(Form):
    username = CharField(required=True)
    password = CharField(required=True, widget=PasswordInput(attrs={'class': 'input_text'}), label='Password')

    def authenticate_user(self):
        username_clean = self.cleaned_data['username']
        password_clean = self.cleaned_data['password']
        auth_user = authenticate(username=username_clean, password=password_clean)
        if auth_user is not None:
            return auth_user
        else:
            return None

class CreditLineForm(ModelForm):
    
    class Meta:
        model = CreditLine
        exclude = ('owner', 'slug', )
        
        
class PaymentPlanForm(ModelForm):
    
    class Meta:
        model = PaymentPlan
        exclude = ('owner', 'credit_line', 'generation_date', 'risk_indicator', 'slug', 'state', )
    

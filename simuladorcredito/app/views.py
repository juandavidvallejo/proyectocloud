# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from app.forms import UserForm, LoginForm, BaseUserForm, CreditLineForm, PaymentPlanForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout
from models import PaymentPlan, UserProfile, CreditLine
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.utils import insert_nonrel, insert_async_message

# Create your views here.
def index(request):
    return render(request, "app/index.html")

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('private'))
    else:
        form_errors = None
        baseform_errors = None
        if request.method == 'POST':  # If the form has been submitted...
            #to update the user.. form = UserForm(request.POST, instance=request.user)
            form = UserForm(request.POST)
            baseform = BaseUserForm(request.POST)
            if form.is_valid() and baseform.is_valid():
                baseuser = baseform.save()
                newprofile = form.save(commit=False)
                newprofile.user = baseuser
                newprofile.save()
                #Custom stuff.....
                insert_nonrel("users", newprofile)
                return HttpResponseRedirect(reverse_lazy('private'))
            else:
                form_errors = form.errors
                baseform_errors = baseform.errors
                return render(request, 'app/signup.html', {'baseform': baseform, 'form': form, 'base_errors': baseform_errors, 'errors': form_errors})
        form = UserForm(request.GET)
        baseform = BaseUserForm(request.GET)
        return render(request, 'app/signup.html', {'baseform': baseform, 'form': form, 'base_errors': baseform_errors, 'errors': form_errors})

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('private'))
    else:
        form_errors = None
        if request.method == 'POST':  # If the form has been submitted...
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.authenticate_user()
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse('private'))
                else:
                    return render(request, 'app/login.html', {'form': form, 'errors': _('Datos invalidos')})
            else:
                form_errors = form.errors
        form = LoginForm(request.GET)
        return render(request, 'app/login.html', {'form': form, 'errors': form_errors})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def public(request, pyme_id):
	pyme = get_object_or_404(UserProfile, slug=pyme_id)
	lineas = CreditLine.objects.filter(owner=pyme)
	return render(request, 'app/public.html', {'lineas': lineas})

def public_plan(request, pyme_id, plan_id):
	form_errors = None
	pyme = get_object_or_404(UserProfile, slug=pyme_id)
	linea = get_object_or_404(CreditLine, slug=plan_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = PaymentPlanForm(request.POST)
		if form.is_valid():
			paymentplan = form.save(commit=False)
			paymentplan.owner = pyme
			paymentplan.credit_line = linea
			paymentplan.save()
			#Custom stuff.....
			insert_nonrel("payment_plans", paymentplan)
			insert_async_message("payment_plans_queue", paymentplan.id)
			return HttpResponseRedirect(reverse('private'))
		else:
			form_errors = form.errors
	form = PaymentPlanForm(request.GET)
	return render(request, 'app/create_new_plan.html', {'form': form, 'errors': form_errors})

@login_required(login_url=reverse_lazy('user_login'))
def private(request):
	profile = request.user.get_profile()
	plans = PaymentPlan.objects.order_by('generation_date').filter(owner=profile)
	lineas = CreditLine.objects.filter(owner=profile)

	paginator = Paginator(plans, 50) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		planes = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		planes = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		planes = paginator.page(paginator.num_pages)
	return render(request, 'app/plans.html', {'objects': planes, 'profile': profile, 'lineas': lineas})

def private_plan(request, plan_id):
	plan = get_object_or_404(PaymentPlan, slug=plan_id)
	#interes = float((plan.credit_line.interest_rate))/100
	interes = plan.credit_line.interest_rate
	return render(request, 'app/plan.html', {'object': plan, 'interes': interes})

@login_required(login_url=reverse_lazy('user_login'))
def create_credit_line(request):
	form_errors = None
	pyme = request.user.get_profile()
	if request.method == 'POST':  # If the form has been submitted...
		form = CreditLineForm(request.POST)
		if form.is_valid():
			creditline = form.save(commit=False)
			creditline.owner = pyme
			creditline.save()
			#Custom stuff.....
			insert_nonrel("credit_lines", creditline)
			return HttpResponseRedirect(reverse('private'))
		else:
			form_errors = form.errors
	form = CreditLineForm(request.GET)
	return render(request, 'app/create_credit_line.html', {'form': form, 'errors': form_errors})

def update_credit_line(request, credit_line_id):
	form_errors = None
	pyme = request.user.get_profile()
	linea = get_object_or_404(CreditLine, slug=credit_line_id)
	if request.method == 'POST':  # If the form has been submitted...
		form = CreditLineForm(request.POST)
		if form.is_valid():
			linea.credit_line_name = form.cleaned_data['credit_line_name']
			linea.interest_rate = form.cleaned_data['interest_rate']
			linea.save()
			return HttpResponseRedirect(reverse('private'))
		else:
			form_errors = form.errors
	form = CreditLineForm(instance=linea)
	return render(request, 'app/create_credit_line.html', {'form': form, 'errors': form_errors})

def delete_credit_line(request, credit_line_id):
	linea = get_object_or_404(CreditLine, slug=credit_line_id)
	#CreditLine.objects.filter(slug=credit_line_id).delete()
	linea.delete()
	return HttpResponseRedirect(reverse('private'))
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import inlineformset_factory
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CustomerForm 
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

# Create your views here.

@unauthenticated_user
def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user=form.save()
				username = form.cleaned_data.get('username')
				group=Group.objects.get(name='customer')

				user.groups.add(group)

				# when user create assign customer to it so it can redirect to user page succesfully
				Customer.objects.create(
					user=user
					)
				messages.success(request, 'Account was created for ' + username)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)	

def logoutUser(request):
	logout(request)
	return redirect('login')	



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):


	# orders=Order.objects.all()
	orders=request.user.customer.order_set.all()
	# customers=Customer.objects.all()
	total_orders=orders.count()
	# total_customers=customers.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='Pending').count()
	context={'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
	
	
	# context={'orders':orders}
	return render(request,'accounts/user.html',context)	

@login_required(login_url='login')
@admin_only
def home(request):
	orders=Order.objects.all()
	customers=Customer.objects.all()
	total_orders=orders.count()
	total_customers=customers.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='Pending').count()
	context={'orders':orders,'customers':customers,'total_customers':total_customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer=request.user.customer
	form=CustomerForm(instance=customer)
	if request.method=="POST":
		form=CustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context={'form':form}
	return render(request,'accounts/account_settings.html',context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
	products=Product.objects.all()
	return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer=Customer.objects.get(id=pk_test)
	orders=customer.order_set.all()
	orders_count=orders.count()
	# this is filtering method in django with form methods
	myFilter=OrderFilter(request.GET,queryset=orders)
	orders=myFilter.qs
	context={'customer':customer,'orders':orders,'orders_count':orders_count,'myFilter':myFilter}
	return render(request,'accounts/customer.html',context)

# def createOrder(request,pk):
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,id):	
	# inlineformset factory is for multiple order input
	OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'), extra=5)
	customer=Customer.objects.get(id=id)
	formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
	# # form=OrderForm(initial={'customer':customer})
	# form=OrderForm()
	if request.method== 'POST':
		# print('printing post',request.POST)
		# form=OrderForm(request.POST,instance=customer)
		# form=OrderForm(request.POST)

		# if form.is_valid():
		# 	form.save()
		formset=OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()	
			return redirect('/')

	# context={'form':form}
	context={'formset':formset}
	return render(request,'accounts/order_form.html',context)
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	order=Order.objects.get(id=pk)
	form=OrderForm(instance=order)
	# customer=Customer.objects.get(id=pk)
	# form=OrderForm(initial={'customer':customer})
	if request.method== 'POST':
		# print('printing post',request.POST)
		
		form=OrderForm(request.POST,instance=order)
		# form=OrderForm(request.POST,instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	context={'form':form}

	# formset=OrderForm(instance=order)
	# print(formset)
	# if request.method== 'POST':
	# 	# print('printing post',request.POST)
	# 	formset=OrderForm(request.POST,instance=order)
	# 	if formset.is_valid():
	# 		formset.save()
	# 		return redirect('/')
	# context={'formset':formset}

	return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	order=Order.objects.get(id=pk)
	if request.method=="POST":
		order.delete()
		return redirect('/')
	context={'item':order}
	return render(request,'accounts/delete.html',context)

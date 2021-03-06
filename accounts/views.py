from django.shortcuts import render,get_object_or_404,redirect
from accounts.models import *
from django.forms import inlineformset_factory
from .forms import *
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


# Create your views here.

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers=Customer.objects.all()

    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()

    context= {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }


    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()

    context={
        'products':products
    }

    return render(request,'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, cust_id):
    customer=get_object_or_404(Customer, pk=cust_id)
    orders=customer.order_set.all()
    total_order=orders.count()

    myFilter=OrderFilter(request.GET, queryset=orders)
    orders=myFilter.qs

    context={
        'customer':customer,
        'orders':orders,
        'total_order':total_order,
        'myFilter':myFilter
    }
    return render(request,'accounts/customers.html',context)
    


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, crt_id):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'), extra=8)
    customer = Customer.objects.get(id=crt_id)
    formset=OrderFormSet(queryset=Order.objects.none() ,instance=customer)  
    #form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        formset=OrderFormSet(request.POST, instance=customer)  
        #form1=OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={
        'formset':formset,
        'customer':customer
    }

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, upd_id):
    order=Order.objects.get(id=upd_id)  
    form=OrderForm(instance=order)

    if request.method=='POST':
        form1=OrderForm(request.POST, instance=order)
        if form1.is_valid():
            form1.save()
            return redirect('/')
    context={
        'formset':form
    }
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, del_id):
    order=Order.objects.get(id=del_id)
    if request.method=='POST':
        order.delete()
        return redirect('/')

    context = {
        'item':order
    }
    return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserFrom()   
    if request.method == 'POST':
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form':form
    }
    return render(request, 'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect.')
    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()    
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    print("ORDERS : ", orders)
    context = {
        'orders' : orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }

    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)
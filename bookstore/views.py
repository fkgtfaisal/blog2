from django.shortcuts import render,redirect
from django.http import HttpResponse 
from .models import *
from .forms import OrderForm , CreateNewUser
from .filters import OrderFilter
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login  , logout 
from django.contrib.auth.decorators import  login_required
from .decorators import notLoggedUsers , allowedUsers, forAdmins
from django.contrib.auth.models import User # Group



def home(requist):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in progress').count()
    out_orders = orders.filter(status='out of order').count()
    context = {'customers': customers,'orders': orders,'t_orders': t_orders,'p_orders': p_orders,
               'd_orders': d_orders,'in_orders': in_orders,'out_orders': out_orders}
    return render(requist, 'bookstore/dashboard.html',context)

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    number_orders = orders.count()

    searchFilter = OrderFilter(request.GET , queryset=orders) # request.GET , queryset=orders
    orders = searchFilter.qs


    context = {'customer': customer ,
               'myFilter': searchFilter,
               'orders': orders,
               'number_orders': number_orders }
    return render(request , 'bookstore/customer.html',context)

def books(requist):
    books = Book.objects.all()
    return render(requist, 'bookstore/books.html', {'books': books})



def profile(requist):
    return render(requist, 'bookstore/profile.html', {'profile': profile})


# def create(request): 
#     form = OrderForm()
    
#     # OrderFormSet = inlineformset_factory(Customer,Order,fields=('book', 'status'),extra=8)
#     # customer = Customer.objects.get(id=pk)
#     # formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
#     # # form = OrderForm()
#     if request.method == 'POST':
#     #    print(request.POST)
#        form = OrderForm(request.POST)
#     #   formset = OrderFormSet(request.POST , instance=customer)
#        if form.is_valid():
#           form.save()
#           return redirect('/')
#     # #context = {'form':form}
#     context = {'form':form}

#     return render(request , 'bookstore/my_order_form.html', context )



def create(request,pk): 
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('book', 'status'), extra = 8)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
    # form = OrderForm()
    if request.method == 'POST':
       # print(request.POST)
      # form = OrderForm(request.POST)
      formset = OrderFormSet(request.POST , instance=customer)
      if formset.is_valid():
           formset.save()
           return redirect('/')
    #context = {'form':form}
    context = {'formset':formset}

    return render(request , 'bookstore/my_order_form.html', context )

# ------------------
def update(request,pk): 
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) 
    if request.method == 'POST': 
       form = OrderForm(request.POST, instance=order)
       if form.is_valid():
           form.save()
         
           return redirect('/')

    context = {'form':form}

    return render(request , 'bookstore/my_order_form.html', context )


def delete(request,pk): 
    order = Order.objects.get(id=pk) 
    if request.method == 'POST':  
        order.delete()
        return redirect('/')

    context = {'order':order}

    return render(request , 'bookstore/delete_form.html', context )



def login(request): 
    context = {}

    return render(request , 'bookstore/login.html', context )

def register(request):   
            form = CreateNewUser()
            if request.method == 'POST': 
                   form = CreateNewUser(request.POST)
                   if form.is_valid():

                       recaptcha_response = request.POST.get('g-recaptcha-response')
                       data = {
                           'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                           'response' : recaptcha_response
                       }
                       r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                       result = r.json()
                       if result['success']:
                           user = form.save()
                           username = form.cleaned_data.get('username')
                           messages.success(request , username + ' Created Successfully !')
                           return redirect('login')
                       else:
                          messages.error(request ,  ' invalid Recaptcha please try again!')  
 
        
            context = {'form':form}

            return render(request , 'bookstore/register.html', context )
from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
from .models import *
from .forms import OrderForm



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

    # searchFilter = OrderFilter(request.GET , queryset=orders)
    # orders = searchFilter.qs


    context = {'customer': customer ,
               'orders': orders,
               'number_orders': number_orders }
    return render(request , 'bookstore/customer.html',context)

def books(requist):
    books = Book.objects.all()
    return render(requist, 'bookstore/books.html', {'books': books})



def profile(requist):
    return render(requist, 'bookstore/profile.html', {'profile': profile})


def create(request): 
    form = OrderForm()
    
    # OrderFormSet = inlineformset_factory(Customer,Order,fields=('book', 'status'),extra=8)
    # customer = Customer.objects.get(id=pk)
    # formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
    # # form = OrderForm()
    if request.method == 'POST':
    #    print(request.POST)
       form = OrderForm(request.POST)
    #   formset = OrderFormSet(request.POST , instance=customer)
       if form.is_valid():
          form.save()
          return redirect('/')
    # #context = {'form':form}
    context = {'form':form}

    return render(request , 'bookstore/my_order_form.html', context )
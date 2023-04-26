from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required  
from .forms import InputForm, AddInventoryForm, UpdateInventoryForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import UserAccount, Inventory, Sale, Order
from .filters import Inventory_Filter
from django.contrib.auth.models import User
from django.contrib import messages

#def index(request):  
 #   return render(request, 'index.html')


def index(request):
    inventories = Inventory.objects.all().order_by('-id')
    inventory_filters = Inventory_Filter(request.GET, queryset = inventories)
    inventories = inventory_filters.qs
    context = {
        'inventories': inventories,
        'inventory_filters': inventory_filters,
    }
    return render(request, "index.html", {'inventories': inventories,
        'inventory_filters': inventory_filters})

def register(request):
    return render(request, 'register.html')

def registration(request):
    #if request.method == 'POST':
    user_name = request.POST['username']
    email = request.POST['user_email']
    password = request.POST['password']
    gender = request.POST['gender']
    user_details = [user_name, email, password, gender]
    #print(user_details)
    if User.objects.filter(username=user_name).first():
        messages.error(request, 'User already exists')
        print(user_name + ' already exists')
        return render(request, 'register.html')
    else:
        user = User.objects.create_user(user_name, email, password)
        #return render(request, 'home.html')
        # messages.success(request, 'User succesfully registered')
        messages.success(request, f'Your account has been created. You can log in now!')
        return redirect('login')
    #return render(request, 'index.html', {'username': username})
    
""" def login_user(request):
    user_name = request.POST['username']
    pwd = request.POST['password']
    if User.objects.filter(username=user_name):
        print(user_name + ' already exists')
        logged_user = authenticate(request, username=user_name, password=pwd)
        if logged_user is not None:
            #login the user
            auth_login(request, logged_user)
            print(user_name + ' ' + 'logged in successfully')
            return redirect('index')
        else:
            # where authentication has failed/ user credentials do not exist
            return render(request, 'login.html')
    else:
        print('User credentials do not exist')
        return render(request, 'login.html')



def login_page(request):
    return render(request, 'login.html') """


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all().order_by('-id')
    inventory_filters = Inventory_Filter(request.GET, queryset = inventories)
    inventories = inventory_filters.qs
    context = {
        'inventories': inventories,
        'inventory_filters': inventory_filters,
    }
    return render(request, "inventory/inventory_list.html", {'inventories': inventories,
        'inventory_filters': inventory_filters})

@login_required
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }
    return render(request, 'inventory/per_product.html', context=context)


def add_product(request):
    
    if request.method == 'POST':
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.sales = int(add_form.data['cost_per_item']) * int(add_form.data['quantity_sold'])
            new_inventory.save()
            return redirect('/')
    else:
        add_form = AddInventoryForm()
    return render(request, 'inventory/inventory_add.html', {'form': add_form})


def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    return redirect('/')

def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        updateForm = UpdateInventoryForm()
        if updateForm.is_valid():
            inventory.name = updateForm.data['name']
            inventory.cost_per_item = updateForm.data['cost_per_item']
            inventory.quantity_in_stock = updateForm.data['quantity_in_stock']
            inventory.quantity_sold = updateForm.data['quantit_sold']
            inventory.received_quantity = updateForm.data['received_quantity']
            inventory.sales = int(inventory.cost_per_item) * int(inventory.quantity_sold)
            inventory.save()
            return redirect('/')
    else:
        updateForm = UpdateInventoryForm()
    context = {
        'form': updateForm
        }
    return render(request, 'inventory/inventory_update.html', context=context)
    

    # def store(request):
    #     context = {

    #     }
    #     return render(request, 'store/store.html', context)


@login_required
def sales_records(request):
    sales = Sale.objects.all()
    total = sum([items.amount_received for items in sales])
    balance = sum([items.get_balance() for items in sales])
    net = total - balance
    return render(request, 'products/all_sales.html', 
                  {'sales': sales,
                  'total': total,
                  'balance': balance,
                  'net': net})

def cart(request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_created(customer=customer, complete=Fales)

        context = {

        }
        return render(request, 'store/cart.html', context)
    
def checkout(request):
        context = {

        }
        return render(request, 'store/checkout.html', context)
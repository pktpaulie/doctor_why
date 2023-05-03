import datetime
import json
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required  
from .forms import InputForm, AddInventoryForm, UpdateInventoryForm, SalesForm, DispenseForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView
from .models import *
from .filters import Inventory_Filter
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    if request.user.is_authenticated:
        user=request.user
        messages.success(request, f'Welcome {user}')
    inventories = Inventory.objects.all().order_by('-id')
    stock = sum([inventory.quantity_in_stock for inventory in inventories])
    inventory_filters = Inventory_Filter(request.GET, queryset = inventories)
    inventories = inventory_filters.qs
    
    cart, created = Cart.objects.get_or_create(complete=False)    
    cartItems = cart.product.all().count()
    context = {
        'inventories': inventories,
        'inventory_filters': inventory_filters,
        'cartItems': cartItems,
        'stock': stock,
    }
    return render(request, "index.html", context)

def register(request):
    return render(request, 'register.html')

def registration(request):
    #if request.method == 'POST':
    user_name = request.POST['username']
    email = request.POST['user_email']
    password = request.POST['password']
    gender = request.POST['gender']
    #user_details = [user_name, email, password, gender]
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


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all().order_by('-id')
    inventory_filters = Inventory_Filter(request.GET, queryset = inventories)
    inventories = inventory_filters.qs
    status = [items.inventory_status() for items in inventories]
    if status == 'Low':
        messages.warning(request, 'Low Stock!', extra_tags='red')

    context = {
        'inventories': inventories,
        'inventory_filters': inventory_filters,
        'status': status,
    }
    return render(request, "inventory/inventory_list.html", context)

@login_required
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }
    return render(request, 'inventory/per_product.html', context=context)

@login_required
def add_product(request):
    
    if request.method == 'POST':
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.sales = int(add_form.data['cost_per_item']) * int(add_form.data['quantity_sold'])
            new_inventory.save()
            messages.success(request, f"{new_inventory.name} added to stock")
            return redirect('/')
    else:
        add_form = AddInventoryForm()
    return render(request, 'inventory/inventory_add.html', {'form': add_form})

@login_required
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.danger(request, f"{inventory.name} deleted")
    return redirect('/')

@login_required
def update_inventory(request, pk):
    #inventory = get_object_or_404(Inventory, pk=pk)
    inventory = Inventory.objects.get(id = pk)
    if request.method == 'POST':
        updateForm = UpdateInventoryForm(data=request.POST)
        if updateForm.is_valid():
            #inventory.name = updateForm.data.get('name')
            new_cost_per_item = int(updateForm.data['cost_per_item'])
            #inventory.quantity_in_stock = int(updateForm.data['quantity_in_stock'])
            #inventory.quantity_sold = updateForm.data.get('quantity_sold')
            inventory.received_quantity = int(updateForm.data['received_quantity'])
            #if inventory.quantity_sold is not None:
            #    inventory.sales += (inventory.cost_per_item) * int(inventory.quantity_sold)
            #inventory.save()
            inventory.quantity_in_stock += inventory.received_quantity
            inventory.cost_per_item = new_cost_per_item
            inventory.save()
            messages.success(request, f"{inventory.name} updated!")
            return redirect('index')
            #return redirect(f"/product/{pk}")
            #return render(request, 'inventory/per_product.html')
    else:
        updateForm = UpdateInventoryForm(instance=inventory)
    context = {
        'form': updateForm
        }
    return render(request, 'inventory/inventory_update.html', {'form': updateForm})
    
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

def cart(request):
    if request.user.is_authenticated:
        #customer = request.user.customer
        #order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order, created = Order.objects.get_or_create(complete=False)
        items = order.orderitem_set.all()
    else:
        items = []

    context = {
        'items': items
    }
    return render(request, 'store/cart.html', context)

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.product.add(product)
        cart.save()
        messages.success(request, f"{product.name} was added to your basket!")
    else:
        
        messages.warning(request, "You must be logged in to add items to your basket.")
        #return redirect('index', inventory_id=product.id)
    return redirect('view_cart')
    #return render(request, 'store/view_cart.html')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, complete=False)
    items = cart.product.all()
    total = sum([item.cost_per_item for item in items])
    cartItems = cart.product.all().count()
    context = {
        'cart': cart,
        'items': items,
        'total': total,
        'cartItems': cartItems,
    }
    return render(request, 'store/view_cart.html', context=context)

@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.product.remove(product)
    cart.save()
    messages.success(request, f"{product.name} was removed from your basket")
    return redirect('view_cart')


def checkout(request):
    dispensed_item = Inventory.objects.all()
    dispense_form = DispenseForm(request.POST)
    if request.user.is_authenticated:
        order, created = Cart.objects.get_or_create(user=request.user, complete=False)
        items = order.product.all()
        cartItems = items.count()
        total = sum([item.cost_per_item for item in items])
        #balance = sum([items.get_balance() for items in sales])
        #customer_balance = total - self.paid_amount
        #return abs(int(customer_balance)) 
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'total':0, 'cartItems':0}
        cartItems = order['total']
        

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'total':total}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['itemId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	product = Inventory.objects.get(id=productId)
	order, created = Order.objects.get_or_create(user=request.user, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		
		order, created = Order.objects.get_or_create(user=request.user, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)


@login_required
def dispense_item(request, pk):
    dispensed_item = Inventory.objects.get(id = pk)
    dispense_form = DispenseForm(request.POST)
    if request.method == 'POST':
        if dispense_form.is_valid():
            new_sale = dispense_form.save(commit = False)
            new_sale = dispensed_item
            new_sale.unit_price = dispensed_item.paid_amount
            new_sale.save()

            # to keep track of stock remaining after sales
            issued_quantity = int(request.POST['quantity'])
            dispensed_item.quantity_in_stock -= issued_quantity
            dispensed_item.save()
            print(dispensed_item.name)
            print(request.POST['quantity'])
            print(dispensed_item.quantity_in_stock)

            return redirect('receipt')
    return render(request, 'cart/checkout.html', {'sales_form': dispense_form})
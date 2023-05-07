from django import forms
from django.forms import ModelForm
from .models import *


class InputForm(forms.Form):
  
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    # roll_number = forms.IntegerField(
                     #help_text = "Enter 6 digit roll number" ) 
    password = forms.CharField(widget = forms.PasswordInput())


# access the models and link the form to the model
class AddInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'category', 'images', 'cost_per_item', 'quantity_in_stock', 'quantity_sold', 'received_quantity']

class UpdateInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['cost_per_item', 'received_quantity']
        autocomplete_fields = ['name']
    
# modeling a form that we shall use to register a sale for a product
class SalesForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'paid_amount', 'bill']

class DispenseForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['customer_name', 'paid_amount']
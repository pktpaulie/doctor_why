from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

# User is used by Django, so we have to find another name for the class
# this is a custom model
class UserAccount(models.Model):
    username = models.CharField(max_length=22, blank=True)
    gender = models.CharField(max_length=6, blank=True)
    email = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=22)
    signup_time = models.DateTimeField(auto_now=True)



class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

class Inventory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    cost_per_item = models.PositiveIntegerField(default=1, null=True, blank=True)
    #quantity_in_stock = models.IntegerField(validators=[MinValueValidator(0)])
    quantity_in_stock = models.IntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    quantity_sold = models.IntegerField(default=1, null=False, blank=False)
    received_quantity = models.PositiveIntegerField(default = 0, null = True, blank = True)
    sales = models.IntegerField(default=0, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    minimum_stock_level = models.IntegerField(default=0, null=False, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateField(auto_now=True)
    batch_number = models.CharField(max_length=100, null=True, blank=True)
    images = models.ImageField(null=True, blank=True)
    
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']

    @property
    def image_url(self):
        try:
            url = self.images.url
        except:
            url = 'static/images/medicine.jpg'
        return url
        # if self.images and hasattr(self.images, 'url'):
        #     return self.images.url
    
    @property
    def get_sales(self):
        sold = self.quantity_sold * self.cost_per_item
        return sold

    def inventory_status(self):
        if self.quantity_in_stock <= self.minimum_stock_level:
            return 'Low'
        return 'OK'
    
    def get_low_stock(self):
        if self.quantity_in_stock <= self.minimum_stock_level:
            return True
        return False

# class UploadImage
#     images = models.ImageField(upload_to='images')

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    #unit_measure = models.CharField(max_length=20, null=True)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


  
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    placed_at = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True) 
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Inventory, on_delete=models.SET_NULL, blank=True, null=True)
    quantity_sold = models.IntegerField(default=1, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    #product = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ManyToManyField(Inventory)
    quantity = models.PositiveIntegerField(default=1, null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    paid_amount = models.IntegerField(default = 0, null = False, blank = True)
    customer_name = models.CharField(max_length=50, null=True, blank=True)

    def get_total(self):
        total = sum([self.quantity * product.cost_per_item for product in self.product.all()])
        # convert total to int
        return int(total)
    
    def get_balance(self):
        balance = self.get_total() - self.paid_amount
        if balance >= 0:
            return (int(balance))
        else:
            return 0

    def __str__(self):
        return f"{self.id}"
    

    """ @property
    def get_cart_total(self):
        total = self.product.cost_per_item * self.quantity
        return "{:,}".format(total) """
    """
    @property
    def get_cart_items(self):
        cartitems = self.all()
        total = sum(self.get_cart_total for item in cartitems)
        return total """
    
    """ @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return total
    
    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
 """

class CartItem(models.Model):
    product = models.ManyToManyField(Inventory)
    quantity = models.PositiveIntegerField(default=1, null=True)
    complete = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)

    @property
    def get_cart_total(self):
        total = self.product.cost_per_item * self.quantity
        return total
    
class Sale(models.Model):
    product = models.ForeignKey(CartItem, on_delete=models.CASCADE, null=True, blank=True)
    #quantity = models.ForeignKey(CartItem, on_delete=models.SET_NULL, null=True, blank = True)
    cost_per_item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank = True)
    paid_amount = models.IntegerField(default = 0, null = False, blank = True)
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    sold_date = models.DateTimeField(auto_now_add=True)
    # = models.ForeignKey(Cart')

    def get_bill(self):
        total_bill = self.product.quantity * self.cost_per_item
        # convert total bill to integer and return value
        return int(total_bill)
    
    def get_balance(self):
        customer_balance = self.get_bill - self.paid_amount
        return abs(int(customer_balance))
    
    def __str__(self):
        return f"{self.customer_name}"

class Wallet(models.Model):
    balance = models.IntegerField(validators=[MinValueValidator(0)])
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
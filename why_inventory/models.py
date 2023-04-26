from django.core.validators import MinValueValidator
from django.db import models
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
    name = models.CharField(max_length=100)
    cost_per_item = models.PositiveIntegerField(null=False, blank=False)
    quantity_in_stock = models.IntegerField(validators=[MinValueValidator(0)])
    quantity_sold = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0)])
    received_quantity = models.PositiveIntegerField(default = 0, null = True, blank = True)
    sales = models.PositiveIntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=255, null=True, blank=True)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateField(auto_now=True)
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

class Sale(models.Model):
    sold_item = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    sold_quantity = models.IntegerField(default = 0, null = False, blank = True)
    unit_price = models.IntegerField(default = 0, null = False, blank = True)
    paid_amount = models.IntegerField(default = 0, null = False, blank = True)
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    sold_date = models.DateTimeField(auto_now_add=True)

    def get_bill(self):
        total_bill = self.sold_quantity * self.unit_price
        # convert total bill to integer and return value
        return int(total_bill)
    
    def get_balance(self):
        customer_balance = self.get_bill - self.paid_amount
        return abs(int(customer_balance))
    
    def __str__(self):
        return self.sold_item.name
    

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Inventory, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    #unit_price = models.PositiveIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Wallet(models.Model):
    balance = models.IntegerField(validators=[MinValueValidator(0)])
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
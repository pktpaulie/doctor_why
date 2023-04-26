import django_filters
from .models import Collection, Product, Inventory


class Product_Filter(django_filters.FilterSet):
    # alter/ manipulate content of another class
    class Meta:
        model = Product
        fields = ['title']

class Category_Filter(django_filters.FilterSet):
    class Meta:
        model = Collection
        fields = ['title']

class Inventory_Filter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Inventory
        fields = ['name']
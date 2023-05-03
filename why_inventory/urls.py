from django.urls import path
from why_inventory import views 
from django.contrib.auth import views as auth_views
from .views import per_product_view, view_cart
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('index/', views.index, name  = 'index'),
    path('home/', views.index, name  = 'home'),
    
    #path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name = 'login'),
    path('register/', views.register, name='register'),
    path('registration/', views.registration, name='registration'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name = 'logout'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name = 'logout'),
    path('inventory', views.inventory_list, name='inventory'),
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.per_product_view, name='per_product'),
    path('add_inventory', views.add_product, name='add_inventory'),
    path('update/<int:pk>', views.update_inventory, name='update_inventory'),
    #path('cart/', views.cart, name='store/cart'),
    path('cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('sales_records/', views.sales_records, name='sales_records'),

    path('delete/<int:pk>',views.delete_inventory, name='delete_inventory'),
    #path('login_user/', views.login_user, name = 'login_user'),
    #path('login_page/', views.login_page, name = 'login_page'),
]


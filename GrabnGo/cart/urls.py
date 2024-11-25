"""
URL configuration for GrabnGo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from cart import views

app_name = "cart"


urlpatterns = [
    path('add_to_cart/<int:i>',views.add_to_cart,name="add_to_cart"),
    path('remove_from_cart/<int:i>',views.remove_from_cart,name="remove_from_cart"),
    path('delete_item_cart/<int:i>',views.delete_item_cart,name="delete_item_cart"),
    path('cart_view',views.cart_view,name="cart_view"),
    path('orderform',views.orderform,name="orderform"),
    path('payment_status/<u>',views.payment_status,name="payment_status"),
    path('order_view',views.order_view,name="order_view"),
]








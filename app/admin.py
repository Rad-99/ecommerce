from django.contrib import admin
from .models import Customer, Product, Cart

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

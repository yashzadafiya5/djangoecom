from django.contrib import admin
from .models import Customer, Product, Order, OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact_number', 'email']
    search_fields = ['name', 'contact_number', 'email']
    list_filter = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'weight']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_number', 'customer', 'order_date', 'address']
    search_fields = ['order_number', 'customer__name', 'address']
    list_filter = ['customer']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    search_fields = ['order__order_number', 'product__name']
    list_filter = ['product']


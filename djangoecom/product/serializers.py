from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Product, Order, OrderItem
from django.utils import timezone



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
        }

    def validate_name(self, value):
        instance = self.instance
        if instance and instance.name == value:
            return value

        if Customer.objects.filter(name=value).exists():
            raise serializers.ValidationError("Customer with this name already exists.")
        return value

    def validate_contact_number(self, value):
        cleaned_number = ''.join(filter(str.isdigit, value))
        
        if len(cleaned_number) != 10:
            raise serializers.ValidationError("Contact number must be a 10-digit number.")

        return cleaned_number

    def validate(self, data):
        if 'contact_number' in data:
            data['contact_number'] = self.validate_contact_number(data['contact_number'])

        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
            'weight': {'validators': []},
        }

    def validate_weight(self, value):
        if value <= 0 or value > 25:
            raise serializers.ValidationError("Weight must be a positive decimal and not more than 25kg.")
        return value

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        return value

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'address', 'order_number']

    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Order date cannot be in the past.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    order_number = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'order_number']

    def get_order_number(self, obj):
        return obj.order.order_number

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        total_weight = product.weight * quantity
        
        existing_order_items = self.context.get('order_items', [])
        
        total_weight += sum(item.product.weight * item.quantity for item in existing_order_items)
        
        if total_weight > 150:
            raise serializers.ValidationError("Order cumulative weight must be under 150kg.")
        
        return data
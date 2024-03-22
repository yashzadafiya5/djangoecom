from rest_framework import generics, serializers, status
from rest_framework.response import Response
from .models import Customer, Product, Order, OrderItem
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from django.db.models import Count, Sum
from django.db.models import Q

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

class OrderItemListAPIView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemCreateAPIView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        serializer.save(order_id=order_id)

class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderListByProductAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        products = self.kwargs.get('products', None)
        if products:
            products_list = products.split(',')
            queryset = Order.objects.filter(order_items__product__name__in=products_list)
            return queryset
        else:
            return Order.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            orders_aggregated = queryset.values('customer', 'order_number', 'order_items__product__name') \
                .annotate(total_quantity=Sum('order_items__quantity'))

            orders_data = {}
            for order in orders_aggregated:
                customer = order['customer']
                order_number = order['order_number']
                product_name = order['order_items__product__name']
                total_quantity = order['total_quantity']

                if (customer, order_number) not in orders_data:
                    orders_data[(customer, order_number)] = {
                        'customer': customer,
                        'order_number': order_number,
                        'order_items': [{ 'product_name': product_name, 'quantity': total_quantity }]
                    }
                else:
                    orders_data[(customer, order_number)]['order_items'].append({
                        'product_name': product_name,
                        'quantity': total_quantity
                    })

            response_data = list(orders_data.values())
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No orders found for the specified products."}, status=status.HTTP_404_NOT_FOUND)


class OrderListByCustomerAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        customer_name = self.kwargs.get('customer', None)
        return Order.objects.filter(customer__name=customer_name)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            orders_data = []
            for order in queryset:
                order_serializer = self.get_serializer(order)
                orders_data.append(order_serializer.data)
            return Response(orders_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No orders found for the specified customer."}, status=status.HTTP_404_NOT_FOUND)
from django.urls import path
from .views import (
    CustomerListCreateAPIView
    , CustomerUpdateAPIView
    , ProductListCreateAPIView
    , OrderListAPIView
    , OrderCreateAPIView
    , OrderUpdateAPIView
    , OrderListByProductAPIView
    , OrderListByCustomerAPIView
    , OrderItemCreateAPIView
    , OrderItemRetrieveUpdateDestroyAPIView
    , OrderItemListAPIView
    
    )

urlpatterns = [
    path('api/customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('api/customers/<int:pk>/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    path('api/products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('api/orders/', OrderListAPIView.as_view(), name='order-list'),
    path('api/orders/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('api/orders/<int:pk>/', OrderUpdateAPIView.as_view(), name='order-update'),
    path('api/orders/customers/<str:customer>/', OrderListByCustomerAPIView.as_view(), name='order-list-by-customer'),
    path('api/orders/<str:products>/', OrderListByProductAPIView.as_view(), name='order-list-by-product'),
    path('api/order-items/create/<int:order_id>/', OrderItemCreateAPIView.as_view(), name='order-item-create'),
    path('api/order-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view(), name='order-item-detail'),
    path('api/order-items/', OrderItemListAPIView.as_view(), name='order-items'),
]

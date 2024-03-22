from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

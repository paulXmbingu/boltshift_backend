from django.contrib import admin
from django.urls import path, include
from product.product_serializer import ProductSerializer
from user.customer_serializer import CustomerSerializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')), # home url path
    path('customer/', include('user.urls')), # registering the customer routes
    path('product/', include('product.urls')) # registering the product routes
]

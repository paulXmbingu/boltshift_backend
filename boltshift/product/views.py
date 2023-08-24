from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from rest_framework import generics
from .product_serializer import ProductSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
# the catalogue page
def ProductCatalogue(request):
    message = "Welcome User"
    return HttpResponse(message)


# the product overview
def ProductOverview(request):
    pass

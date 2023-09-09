from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from .serializer import ProductSerializer
from .models import Product


# Responsible for getting all products in the database
# Renders products in the catalogue page
class ProductCatalogue(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        pass

# Renders details of a specific product
# in the product overview page
class ProductOverview(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        pass

from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ProductSerializer
from .models import Product


# Responsible for getting all products in the database
# Renders products in the catalogue page
class ProductCatalogue(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        """
            # Displaying all products
            displayed: 
        """
        pass

# Renders details of a specific product
# in the product overview page
class ProductOverview(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        pass

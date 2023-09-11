from .serializer import Vendor
from rest_framework import viewsets
from .serializer import VendorRegistrationAPI
from product.models import Product


class VendorRegistration(viewsets.ModelViewSet):
    serializer_class = VendorRegistrationAPI
    queryset = Vendor.objects.all()
        
class VendorLogin(viewsets.ModelViewSet):
    def validate(self, data):
        pass

class VendorAddProduct(viewsets.ModelViewSet):
    def post(self, request):
        pass

class VendorProductView(viewsets.ModelViewSet):
    def get(self, request):
        pass

    def income(self, request):
        pass
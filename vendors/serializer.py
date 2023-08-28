from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['image', 'warranty_period', 'response_time', 'shipping_time', 'user', 'address']
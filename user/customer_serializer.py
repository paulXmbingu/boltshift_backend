from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.Serializer):
    class Meta:
        model = Customer
        # fields = "__all__"
        exclude = ('password', 'profile_img')

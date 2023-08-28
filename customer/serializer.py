from rest_framework import serializers
from .models import CustomUser

class SerializeCustomer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined']
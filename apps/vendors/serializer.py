from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Vendor

# username min_length
LENGTH = 6

class VendorRegistrationAPI(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(
        min_length = LENGTH,
        error_messages = {
            "min_length": f"Username must be {LENGTH} characters long"
        }
    )

    class Meta:
        model = Vendor
        exclude = ['first_name', 'last_name', 'image', 'warranty_period', 'response_time', 'shipping_time', 'user', 'address', 'rating', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined']

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        vendor = Vendor.objects.create(
            vendor_name = validated_data["vendor_name"],
            email = validated_data["email"],
            description = validated_data["description"],
            username = validated_data["username"],
            warranty_period = 0
        )
        vendor.set_password(validated_data["password"])

        vendor.save()

        return vendor

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
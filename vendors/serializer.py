from rest_framework import serializers
from .models import Vendor
from hashed import hash_password

# password min length
MIN_LENGTH = 8

class VendorRegistrationAPI(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        min_length = MIN_LENGTH,
        error_messages = {
            "min_length": f"Passwords must be {MIN_LENGTH} characters long"
        }
    )
    password2 = serializers.CharField(
        write_only = True,
        min_length = MIN_LENGTH,
        error_messages = {
            "min_length": f"Passwords must be {MIN_LENGTH} characters long"
        }
    )

    class Meta:
        model = Vendor
        exclude = ['image', 'warranty_period', 'response_time', 'shipping_time', 'user', 'address', 'rating']

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        password_hashed = hash_password(validated_data["password"], validated_data["password2"])

        vendor = Vendor.objects.create(
            vendor_name = validated_data["vendor_name"],
            email = validated_data["email"],
            description = validated_data["description"],
            password = password_hashed,
            warranty_period = 1
        )
        vendor.save()

        return vendor

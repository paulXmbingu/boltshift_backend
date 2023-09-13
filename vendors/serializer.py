from rest_framework import serializers
from .models import Vendor
from hashed import hash_password

# password min length
MIN_LENGTH = 8
# username min_length
LENGTH = 6

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
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        password_hashed = hash_password(validated_data["password"], validated_data["password2"])

        vendor = Vendor.objects.create(
            vendor_name = validated_data["vendor_name"],
            email = validated_data["email"],
            description = validated_data["description"],
            username = validated_data["username"]
        )
        vendor.set_password(password_hashed)

        vendor.save()

        return vendor

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
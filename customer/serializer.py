from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.password_validation import validate_password
from .models import Customer

USERNAME_LENGTH = 6

# Session Token
# Handled during registration, login, logout
class CustomerTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user: Customer) -> Token:
        return super().get_token(user)

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    username = serializers.CharField(
        min_length = USERNAME_LENGTH,
        error_messages = {
            "min_length": f"Username must be {USERNAME_LENGTH} characters long"
        }
    )

    class Meta:
        model = Customer
        exclude = ['image', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'payment', 'address', 'is_active', 'cid']

    # data validation
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    # saving validated data
    def create(self, validated_data):
        user = Customer.objects.create(
            username = validated_data["username"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            email = validated_data["email"],
            gender = validated_data["gender"],
            is_active = True
        )
        user.set_password(validated_data["password"])

        # saving new user
        user.save()

        return user

# input validation serializer    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

# acount setting
class UpdateUserAccount(serializers.Serializer):
    # the basic details
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    updated_phonenumber = serializers.CharField()
    email = serializers.EmailField()
    gender = serializers.CharField()

    # address details
    apartment_details = serializers.CharField()
    street_address = serializers.CharField()
    country = serializers.CharField()
    city_town = serializers.CharField()
    postal_code = serializers.CharField()

    # to update password
    old_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Customer

    # data.passwords validation
    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def update(self, validated_data):
        # updating user credentials
        user = Customer.objects.bulk_update(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            dob = validated_data['dob'],
        )

        return user
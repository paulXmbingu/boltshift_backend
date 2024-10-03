from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.password_validation import validate_password
from .models import Customer, UserAddress, UserCardInformation, UserType

USERNAME_LENGTH = 6

# Session Token
# Handled during registration, login, logout
# Returns a user object enclosed within a unique token
class CustomerTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user: Customer) -> Token:
        return super().get_token(user)

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    username = serializers.CharField(
        min_length = USERNAME_LENGTH,
        error_messages = {
            "min_length": f"Username must be {USERNAME_LENGTH} characters long"
        }
    )

    class Meta:
        model = Customer
        exclude = ['image', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'is_active', 'cid']

    # data validation
    def validate(self, data):
        if data["password"] != data["password2"]:
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


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCardInformation
        fields = ['account_number', 'provider']

    def validate_account_number(self, value):
        if value < 0:
            raise serializers.ValidationError('Account number must be provided')
        return value 
    
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['streetname', 'county', 'city', 'country', 'apartment_complex',]

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['is_customer', 'is_vendor', 'user_id',]

# account setting
class UserAccountSerializer(serializers.ModelSerializer):
    payment = UserPaymentSerializer(source='userpayment_set', many=True, read_only=True)
    address = UserAddressSerializer(source='useraddress_set', many=True, read_only=True)
    usertype = UserTypeSerializer(source='usertype_set', many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('cid', 'first_name', 'last_name', 'email', 'username', 'image', 'gender', 'phonenumber_primary', 'phonenumber_secondary', 'address', 'payment', 'usertype',)

class UpdateUserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'username', 'image', 'gender', 'phonenumber_primary', 'phonenumber_secondary']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.image = validated_data.get('image', instance.image)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phonenumber_primary = validated_data.get('phonenumber_primary', instance.phonenumber_primary)
        instance.phonenumber_secondary = validated_data.get('phonenumber_secondary', instance.phonenumber_secondary)
        instance.save()
        
        return instance

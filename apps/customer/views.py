from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .serializer import RegistrationSerializer, LoginSerializer, CustomerTokenObtainSerializer
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout
from rest_framework.response import Response
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from .serializer import RegistrationSerializer, LoginSerializer, UpdateUserAccountSerializer, UserAccountSerializer, UserAddressSerializer, UserPaymentSerializer, UserTypeSerializer
from .models import Customer, UserAddress, UserCardInformation

class CustomerTokenObtainView(TokenObtainSerializer):
    serializer_class = CustomerTokenObtainSerializer

class CustomerRegistration(APIView):
    def post(self, request, format=None):
        user_serializer = RegistrationSerializer(data=request.data)
        
        with transaction.atomic():
            
            if user_serializer.is_valid():

                user_instance = user_serializer.save(**request.data)

                # user type
                user_type = request.data.get('user_type')
                user_type_data = {'user_id': user_instance.id, 'is_customer': user_type.get('is_customer'), 'is_vendor': user_type.get('is_vendor')}
                user_type_serializer = UserTypeSerializer(data=user_type_data)
                if user_type_serializer.is_valid():
                    user_type_serializer.save()

                # Create authentication token
                _, token = AuthToken.objects.create(user_instance)

                response_data = {
                    'user_id': user_instance.id,
                    'username': user_instance.username,
                    'token': token,
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
            
            errors = {}
            errors.update(user_serializer.errors)

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLogin(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        try:
            user_instance = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if check_password(password, user_instance.password):
            _, token = AuthToken.objects.create(user_instance)
            return Response({
                    'user_id': user_instance.id,
                    'username': user_instance.username,
                    'token': token,
                })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
               
class CustomerLogout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            request.auth.delete()
            logout(request)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)
    

class CustomerDeleteAccount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        customer = get_object_or_404(Customer, email=user.email)
        customer.soft_delete()
        logout(request)
        return Response({"message": "Account Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class CustomerAccountSettings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserAccountSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateUserAccountSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_address(self, request, *args, **kwargs):
        user = request.user
        
        address_id = request.POST.get('address_id')

        address = UserAddress.objects.get_object_or_404(id=address_id)

        # check if address belongs to the user
        if address.user_id_id == user.id: 
            return Response({'Error': 'Error Occured'}, status=status.HTTP_400_BAD_REQUEST)

        address_serializer = UserAddressSerializer(address, data=request.data, partial=True)
        address_serializer.is_valid(raise_exception=True)
        address_serializer.save()
        return Response(address_serializer.data, status=status.HTTP_200_OK)

    def update_payment(self, request, *args, **kwargs):
        user = request.user
        payment_serializer = UserPaymentSerializer(user.payment, data=request.data, partial=True)
        payment_serializer.is_valid(raise_exception=True)
        payment_serializer.save()
        return Response(payment_serializer.data, status=status.HTTP_200_OK)

class CustomerShopping(APIView):
    pass

class CustomerWishlist(APIView):
    allowed_methods = ['DELETE', 'POST', 'GET']

class CustomerCheckout(APIView):
    allowed_methods = ['GET', 'POST']

class UserPaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payments = UserCardInformation.objects.all()
        serializer = UserPaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user_id'] = request.user.id
        serializer = UserPaymentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAddressAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        addresses = UserAddress.objects.filter(user=request.user)
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        data['user_id'] = request.user.id
        serializer = UserAddressSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
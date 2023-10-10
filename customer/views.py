from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import CustomUser, UserAddress, UserPayment
from rest_framework.views import APIView
from .serializer import RegistrationSerializer, LoginSerializer, UserAddressSerializer, UserPaymentSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.shortcuts import get_object_or_404
import logging

log = logging.getLogger(__name__)

def index(request):
    return HttpResponse("<h2>Welcome to <b><i>Boltshift E-commerce</i></b></h2>")


class CustomerRegistration(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()

class CustomerLogin(APIView):
    allowed_methods = ['POST']

    # deseralizing the data
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # user authentication
            user = authenticate(username=email, password=password)
            
            if user is not None:
                login(request, user)
                return Response(
                    {
                        'message': 'Login Successful',
                        'user_cid': user.cid
                    },
                    status=status.HTTP_200_OK
                )
            else:
                log.warning(f"Login failed for email: {email}")
                return Response(
                    {'message': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               
class CustomerLogout(APIView):
    # ensure that only logged in users are able to access this
    permission_classes = [IsAuthenticated]
    allowed_methods = ['POST']

    def post(self, request, format=None):
        # logout user
        logout(request)
        # redirect to home page after login out
        redirect_url = reverse("home")
        result = {
            'message': "User logout successfully",
            'redirect_url': redirect_url
        }
        return Response(
            result,
            status=status.HTTP_200_OK
        )

# delete user account
class CustomerDeleteAccount(APIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = ['DELETE']
    
    def delete(self, request, cid):
        customer = get_object_or_404(CustomUser, cid=cid)
        customer.soft_delete()
        logout(customer)
        redirect_url = reverse("home")
        return Response(
            {
                "message": "Account Deleted Successfully",
                "redirect_url": redirect_url
            },
            status=status.HTTP_204_NO_CONTENT
        )
    
# user account settings update
class CustomerAccountSettings(APIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = ['UPDATE']

class CustomerShopping(APIView):
    permission_classes = [IsAuthenticated]

class CustomerWishlist(APIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = ['DELETE', 'POST', 'GET']

class CustomerCheckout(APIView):
    allowed_methods = ['GET', 'POST']

class UserPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payments = UserPayment.objects.all()
        serializer = UserPaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = UserPaymentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserAddressAPIView(APIView):
    def get(self, request, format=None):
        addresses = UserAddress.objects.all()
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
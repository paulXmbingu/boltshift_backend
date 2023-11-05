from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import Customer
from rest_framework.views import APIView
from .serializer import RegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from django.urls import reverse
from django.shortcuts import get_object_or_404

def index(request):
    return HttpResponse("<h2>Welcome to <b><i>Boltshift E-commerce</i></b></h2>")


class CustomerRegistration(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = Customer.objects.all()

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
                        'message': 'Login Successful for %s' % user.email,
                        'user_cid': user.cid
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               
class CustomerLogout(APIView):
    # ensure that only logged in users are able to access this
    allowed_methods = ['POST']

    def post(self, request, format=None):
        # logout user
        logout(request)
        # redirect to home page after login out
        redirect_url = reverse("home")
        result = {
            'message': "Logout Successfull",
            'redirect_url': redirect_url
        }
        return Response(
            result,
            status=status.HTTP_200_OK
        )

# delete user account
class CustomerDeleteAccount(APIView):
    allowed_methods = ['DELETE']
    
    def delete(self, request, cid):
        customer = get_object_or_404(Customer, cid=cid)
        customer.soft_delete()
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
    allowed_methods = ['UPDATE']

class CustomerShopping(APIView):
    pass

class CustomerWishlist(APIView):
    allowed_methods = ['DELETE', 'POST', 'GET']

class CustomerCheckout(APIView):
    allowed_methods = ['GET', 'POST']
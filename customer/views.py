from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import CustomUser
from rest_framework.views import APIView
from .serializer import RegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import logging

log = logging.getLogger(__name__)

def index(request):
    return HttpResponse("<h2>Welcome to <b><i>Boltshift E-commerce</i></b></h2>")


class CustomerRegistrationAPI(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()

class CustomerLoginAPI(APIView):
    allowed_methods = ['POST']

    # deseralizing the data
    @csrf_exempt
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # user authentication
            user = authenticate(request, username=email, password=password)
            print(f"User: {user}")

            if user is not None:
                login(request, user)
                log.info(f"Email: {email}, Password: {password}")
                return Response(
                    {
                        'message': 'Login Sucessful',
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
               
class CustomerLogoutAPI(APIView):
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
class CustomerDeleteAccountAPI(APIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = ['POST']
    queryset = CustomUser.objects.all()

    def post(self, request):
        # getting customer unique id
        cid = request.data.get('cid', [])
        if cid is not None:
            # getting corresponding user
            user = self.queryset.filter(cid__in=cid)
            # deleting user
            user.delete()
            redirect_url = reverse('home')
            return Response(
                {
                    'message': "User Account Deleted Successfully",
                    'redirect_url': redirect_url
                },
                status=status.HTTP_200_OK
            )
from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import CustomUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from .serializer import RegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def index(request):
    return HttpResponse("<h2>Welcome to <b><i>Boltshift E-commerce</i></b></h2>")


class CustomerRegistrationAPI(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()

    
class CustomerLoginAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # deseralizing the data
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # user authentication
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return Response(
                    {
                        'message': 'Login Sucessful',
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
        
class CustomerLogoutAPI(APIView):
    # ensure that only logged in users are able to access this
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # logout user
        logout(request)
        return Response(
            {
                'message': "User logout successfully"
            },
            status=status.HTTP_200_OK
        )
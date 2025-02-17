from .serializer import Vendor
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import VendorRegistrationAPI, LoginSerializer
from product.models import Product
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class VendorRegistration(viewsets.ModelViewSet):
    serializer_class = VendorRegistrationAPI
    queryset = Vendor.objects.all()
        

class VendorLoginAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(self.request, username=email, password=password)

            if user is not None:
                login(request, user)
                return Response(
                    {
                        'message': 'Login successful'
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
        
class VendorLogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response(
            {
                'message': "User logout successfully"
            },
            status=status.HTTP_200_OK
        )

class VendorAddProduct(viewsets.ModelViewSet):
    def post(self, request):
        pass

class VendorProductView(viewsets.ModelViewSet):
    def get(self, request):
        pass

    def income(self, request):
        pass
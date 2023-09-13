from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from rest_framework import viewsets
from .models import CustomUser
from .serializer import RegistrationSerializer


def index(request):
    return HttpResponse("<h2>Welcome to <b><i>Boltshift E-commerce</i></b></h2>")


class CustomerRegistrationAPI(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()


class CustomerLoginAPI(viewsets.ModelViewSet):
    user = CustomUser.objects.all()
    
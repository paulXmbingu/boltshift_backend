from django.urls import path, include
from . import views
from rest_framework import routers

signup = routers.DefaultRouter()
signup.register("", views.CustomerRegistrationAPI, 'sign-up')

urlpatterns = [
    path('api/sign-up', include(signup.urls)),
    path('', views.index, name='home'),
]
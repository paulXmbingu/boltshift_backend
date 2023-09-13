from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("sign-up", views.CustomerRegistrationAPI, 'sign-up')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login', views.CustomerLoginAPI.as_view(), name='login'),
    path('', views.index, name='home'),
]
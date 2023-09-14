from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("sign-up", views.CustomerRegistrationAPI, 'sign-up')

urlpatterns = [
    path('login/', views.CustomerLoginAPI.as_view(), name='login'),
    path('delete-account', views.CustomerDeleteAccountAPI.as_view(), name='delete'),
    path('logout', views.CustomerLogoutAPI.as_view(), name='logout'),
    path('', views.index, name='home'),
] + router.urls
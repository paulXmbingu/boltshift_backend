from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("sign-up", views.CustomerRegistrationAPI, 'sign-up')

urlpatterns = [
    path('/', include(router.urls)),
    path('login', views.CustomerLoginAPI.as_view(), name='login'),
    path('logout', views.CustomerLogoutAPI.as_view(), name='logout'),
    path('', views.index, name='home'),
]
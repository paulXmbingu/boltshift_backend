from django.urls import path
from . import views
from rest_framework import routers

app_name = 'vendors'

router = routers.DefaultRouter()
router.register("register", views.VendorRegistration, 'register')
router.register("add-product", views.VendorAddProduct, 'add')
router.register("overview", views.VendorProductView, 'view')

urlpatterns = [
    path('login', views.VendorLoginAPI.as_view(), name='vendor-login'),
    path('logout', views.VendorLogoutAPI.as_view(), name='vendor-logout')
] + router.urls

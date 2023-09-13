from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("", views.VendorRegistration, 'register')
router.register("", views.VendorAddProduct, 'add')
router.register("", views.VendorProductView, 'view')

urlpatterns = [
    path('vendor-register', include(router.urls)),
    path('vendor-login', views.VendorLoginAPI.as_view(), name='vendor-login'),
    path('vendor-logout', views.VendorLogoutAPI.as_view(), name='vendor-logout')
]
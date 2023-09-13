from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("register", views.VendorRegistration, 'register')
router.register("add-product", views.VendorAddProduct, 'add')
router.register("vendor-products", views.VendorProductView, 'view')

urlpatterns = [
    path('register', include(router.urls)),
    path('vendor-login', views.VendorLoginAPI.as_view(), name='vendor-login')
]
from django.urls import path
from . import views

urlpatterns = [
    path('api-vendor/', views.VendorAPI.as_view(), name='vendor_api')
]
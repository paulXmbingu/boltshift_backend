from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'vendor', views.VendorAPI, 'vendor')

urlpatterns = [
    path('api-vendor/', include(router.urls))
]
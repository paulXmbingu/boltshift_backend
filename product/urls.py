from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("", views.ProductCatalogue, "catalogue")
router.register("", views.ProductOverview, "overview")

urlpatterns = [
    path('', include(router.urls))
]
from django.urls import path, include
from rest_framework import routers
from . import views

catalogue = routers.DefaultRouter()
catalogue.register("", views.ProductCatalogue, "catalogue")

overview = routers.DefaultRouter()
overview.register("", views.ProductOverview, "overview")

urlpatterns = [
    path('productsCatalogue/', include(catalogue.urls), name="catalogue"),
    path('productOverview/', include(overview.urls))
]
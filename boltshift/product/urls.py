from django.urls import path
from . import views

urlpatterns = [
    path('productCatalogue/', views.ProductCatalogue, name='product_catalogue'),
    path('productOverview/', views.ProductOverview, name='product_overview')
]
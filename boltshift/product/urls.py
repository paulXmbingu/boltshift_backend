from django.urls import path
from . import views

urlpatterns = [
    path('product_api/', views.ProductList.as_view(), name='product_api'),
    path('productCatalogue/', views.ProductCatalogue, name='product_catalogue'),
    path('productOverview/', views.ProductOverview, name='product_overview')
]
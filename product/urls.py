from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('catalogue/', views.ProductCatalogue.as_view(), name='catalogue'),
    path('catalogue/<str:pid>/', views.GetProductDetail.as_view(), name='product_detail'),
    path('product/details/<str:pid>/', views.GetProductDetail.as_view(), name='product_detail'),
]


from django.urls import path, include
from rest_framework import routers
from . import views
from utils.utils import save_top_categories


urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('catalogue/', views.ProductCatalogue.as_view(), name='catalogue'),
    path('details/', views.GetProductDetail.as_view(), name='product_detail'),
    
    # save the top product categories
    #save_top_categories()
]
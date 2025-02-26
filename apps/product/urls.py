from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('catalogue/', views.ProductCatalogue.as_view(), name='catalogue'),
    path('catalogue/<str:pid>/', views.GetProductDetail.as_view(), name='product_detail'),
    path('product/details/<str:pid>/', views.GetProductDetail.as_view(), name='product_detail'),
    path('brands/', views.BrandView.as_view(), name='brands'),
    path('categories/', views.CategoryView.as_view(), name='all_categorys'),
    path('categories/<int:category_id>/', views.CategoryView.as_view(), name='single_category'),
    path('inventory/', views.InventoryView.as_view(), name='inventories'),
    path('orders/', views.ProductOrderView.as_view(), name = 'orders'),
    path('reviews/', views.ProductReviewView.as_view(), name = 'reviews' ),
    path('tags/', views.ProductTagView.as_view(), name = 'tags' ),
    path('features/', views.ProductFeatureView.as_view(), name = 'product_features'),
    path('features_mappings/', views.ProductFeatureMappingView.as_view(), name = 'product_features_mappimgs'),
    path('wishlist/',views.Wishlistview.as_view(),name = 'wishlist')
]

from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("sign-up", views.CustomerRegistration, 'sign-up')

urlpatterns = [
    path('login/', views.CustomerLogin.as_view(), name='login'),
    path('delete-account/<str:cid>/soft-delete', views.CustomerDeleteAccount.as_view(), name='delete'),
    path('logout', views.CustomerLogout.as_view(), name='logout'),
    path('', views.index, name='home'),
    path('checkout', views.CustomerCheckout.as_view(), name='checkout'),
    path('account', views.CustomerAccountSettings.as_view(), name='account'),
    path('wishlist', views.CustomerWishlist.as_view(), name='wishlist'),
    path('shopping', views.CustomerShopping.as_view(), name='shopping')
] + router.urls
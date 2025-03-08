from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = 'customer'

def redirect_url(request):
    return redirect("/product/")

urlpatterns = [
    path('', redirect_url),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("sign-up/", views.CustomerRegistration.as_view(), name='sign-up'),
    path('login/', views.CustomerLogin.as_view(), name='login'),
    path('logout', views.CustomerLogout.as_view(), name='logout'),
    path('delete-account', views.CustomerDeleteAccount.as_view(), name='delete'),
    path('checkout', views.CustomerCheckout.as_view(), name='checkout'),
    path('account-settings/', views.CustomerAccountSettings.as_view(), name='account'),
    path('account-settings-user/', views.CustomerAccountSettings.as_view(), name='account-user'),
    path('account-settings-address/', views.CustomerAccountSettings.as_view(), {'put': 'update_address'}, name='account-address'),
    path('account-settings-payment/', views.CustomerAccountSettings.as_view(), {'put': 'update_payment'}, name='account-user-payment'),
    path('wishlist', views.CustomerWishlist.as_view(), name='wishlist'),
    path('shopping', views.CustomerShopping.as_view(), name='shopping'),
    path('createaddress/', views.UserAddressAPIView.as_view(), name='create_user_address'),
    path('createpayment/', views.UserPaymentView.as_view(), name='create_user_payment'),
]

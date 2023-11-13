from django.urls import path
from . import views

urlpatterns = [
    path("sign-up/", views.CustomerRegistration.as_view(), name='sign-up'),
    path('login/', views.CustomerLogin.as_view(), name='login'),
    path('delete-account', views.CustomerDeleteAccount.as_view(), name='delete'),
    path('logout', views.CustomerLogout.as_view(), name='logout'),
    path('', views.index, name='home'),
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
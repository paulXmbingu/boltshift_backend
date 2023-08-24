from django.urls import path
from . import views

urlpatterns = [
    # api handling
    path('customer_api/', views.CustomerList.as_view(), name='customer_api'),
    path('', views.HomePage, name='home'),
    path('registration/', views.UserRegistration, name='register'),
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogout, name='logout'),
    path('passwordReset/', views.UserPasswordReset, name='password_reset'),
    path('accountSettings/', views.UserAccountSettings, name='account_settings'),
    path('userProfile/', views.UserProfile, name='user_profile'),
    path('userShoppingCart/', views.UserShoppingCart, name='shopping_cart'),
    path('userWishlist/', views.UserWishlist, name='wishlist'),
    path('userCheckout/', views.UserProductCheckout, name='product_checkout'),
    path('userProductOrders/', views.UserProductOrders, name='product_orders'),
    path('userPaymentMethod/', views.UserPaymentMethod, name='payment_method')
]
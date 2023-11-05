from rest_framework_simplejwt.views import (
    TokenObtainPairView, # obtaining a token
    TokenRefreshView, # refreshing the obtained token
    TokenVerifyView # verifying the obtained token
)
from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("sign-up", views.CustomerRegistration, 'sign-up')

urlpatterns = [
    # tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', views.CustomerLogin.as_view(), name='login'),
    path('delete-account/<str:cid>/soft-delete', views.CustomerDeleteAccount.as_view(), name='delete'),
    path('logout', views.CustomerLogout.as_view(), name='logout'),
    path('', views.index, name='home'),
    path('checkout', views.CustomerCheckout.as_view(), name='checkout'),
    path('account', views.CustomerAccountSettings.as_view(), name='account'),
    path('wishlist', views.CustomerWishlist.as_view(), name='wishlist'),
    path('shopping', views.CustomerShopping.as_view(), name='shopping')
] + router.urls
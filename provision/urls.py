from django.urls import path
from . import views

urlpatterns = [
    path("shopping_sesh/", views.ShoppingSessionView.as_view(), name='shoppingsesh'),
    path("shopping_cart/", views.CartSessionView.as_view(), name='shoppingCartItem'),
]
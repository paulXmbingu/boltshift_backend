from rest_framework import serializers
from .models import ShoppingSession, CartItem

class ShoppingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingSession
        exclude = ('created_at', 'id')

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ('created_at', 'id')
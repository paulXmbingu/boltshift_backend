from django.contrib import admin
from .models import (CartItem, ShoppingSession,)

@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id']

@admin.register(ShoppingSession)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'total']

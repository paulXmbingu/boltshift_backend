from django.contrib import admin
from .models import (
    Customer,
    UserPayment,
    UserAddress,
    ProductReview,
    CartItem,
    ShoppingSession,
    ProductOrders
)

@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name']
    search_fields = ('email', 'username', 'cid')
    readonly_fields = ['image_tag']

@admin.register(UserAddress)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['addr1',]
    search_fields = ['city', 'country',]
    readonly_fields = ['addr1', 'addr2', 'city', 'country']

@admin.register(UserPayment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'provider']
    search_fields = ['provider']
    readonly_fields = ['account_number', 'provider']

@admin.register(ProductReview)
class AdminReview(admin.ModelAdmin):
    list_display = ['review_title', 'review_rating']
    readonly_fields = ['review_screenshots']

@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id']

@admin.register(ShoppingSession)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'total']

@admin.register(ProductOrders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['ord_id', 'item_number', 'status']
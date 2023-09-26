from django.contrib import admin
from .models import(
    Product,
    CartItem,
    Category,
    Image,
    Inventory,
    Discount,
    ShoppingSession,
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'pid',]
    list_filter = ['title',]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['img_id', 'product_id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['inv_id', 'quantity']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percent']

@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id']

@admin.register(ShoppingSession)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'total']
from django.contrib import admin
from .models import(
    Product,
    Category,
    ProductPhotos,
    Inventory,
    Discount,
    ProductReview,
    ProductOrders
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_id',]
    list_filter = ['name',]

@admin.register(ProductPhotos)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'image', 'image_url']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_choice']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['inventory_id', 'quantity']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percent']

@admin.register(ProductReview)
class AdminReview(admin.ModelAdmin):
    list_display = ['review_title', 'review_rating']
    readonly_fields = ['review_tag']

@admin.register(ProductOrders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'item_number', 'status']
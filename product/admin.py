from django.contrib import admin
from .models import(
    Product,
    Category,
    ProductImage,
    Inventory,
    Discount,
    ProductReview,
    ProductOrders
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'pid',]
    list_filter = ['title',]

@admin.register(ProductImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['img_id', 'product_id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'cat_id']

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['inv_id', 'quantity']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percent']

@admin.register(ProductReview)
class AdminReview(admin.ModelAdmin):
    list_display = ['review_title', 'review_rating']
    readonly_fields = ['review_screenshots']

@admin.register(ProductOrders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['ord_id', 'item_number', 'status']
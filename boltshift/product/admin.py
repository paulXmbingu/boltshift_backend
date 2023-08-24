from django.contrib import admin
from .models import Product, Category, Details

# registering the Product model to the admin dashboard
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'style', 'price', 'category', 'color', 'stock')
    list_filter = ('category', 'title', 'style', 'color')
    search_fields = ('title',)


# registering the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    search_fields = ('category',)


# the Details model
@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    list_display = ('dimensions', 'model_number', 'department', 'manufacturer', 'asin', 'country_of_origin', 'seller_rank')
    search_fields = ('model_number', 'manufacturer', 'asin',)

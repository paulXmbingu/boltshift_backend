from rest_framework import serializers
from .models import Product, ProductImage, Category, Inventory, Discount, PopularProduct

class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        exclude = ('image')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class PopularProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularProduct
        fields = ['pop_id', 'category', 'popularity_count']
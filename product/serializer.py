from rest_framework import serializers
from .models import Product, ProductPhotos, Category, Inventory, Discount, PopularProduct, ProductReview

class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        exclude = '__all__'

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

class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = '__all__'

class PopularProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularProduct
        fields = ['pop_id', 'category', 'popularity_count']
        
class ProductReviewSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields ='__all__'
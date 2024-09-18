from rest_framework import serializers
from .models import  *

class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        exclude = '__all__'

class CategorySerializer (serializers.ModelSerializer):
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

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class PopularProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularProduct
        fields = ['pop_id', 'category', 'popularity_count']
        
class ProductReviewSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields ='__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_id','name','description']
        
class ProductOrdersSerializer(serializers.ModelSerializer):
    model =ProductOrders
    field = ['order_id', "item_number", 'status']
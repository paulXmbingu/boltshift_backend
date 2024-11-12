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
    class Meta:
        model =ProductOrders
        fields = '__all__'

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'
        

class ProductTagMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTagMapping
        fields = '__all__'       

class WishlistSeializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['product_id', 'user_id', 'wishlist_id']       
        
'product features'  
class ProductFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = '__all__'     

'feature mappings'     
class ProductFeatureMappingSerializer(serializers.ModelField):
    class Meta:
        model = ProductFeatureMappings
        fields = '__all__'   
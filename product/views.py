from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import ProductSerializer, PopularProductSerializer, ProductReviewSerialzer
from .models import Product, PopularProduct, ProductReview

from knox.auth import TokenAuthentication

from utils.utils import save_top_categories

# Base Class for unified Responses and Custom Validation Messages
class RequestValidation(APIView):
    authentication_classes = [TokenAuthentication]

    def validate_input_data(self, required_fields, data):
        """
            Validate input data for all Endpoints
        """
        # check for the presence of the required fields
        missing_fields = [field for field in required_fields if data.get(field) is None or data.get(field) == '']

        if missing_fields:
            return self.build_response('Error', f'Missing required fields: {",".join(missing_fields)}', status.HTTP_400_BAD_REQUEST)

  # build responses
    def build_response(self, message, result, status):
        '''
            To build Unified Responses
        '''
        data = {
            "message": message,
            "result": result
        }
        return Response(data, status=status)
        
# default homepage
# default page with the website loads
class HomePage(RequestValidation):
    def get(self, request):
        save_top_categories()
        return self.featured_products()

    def popular_categories(self):
        serializer_class = PopularProductSerializer
        queryset = PopularProduct.objects.all()
        
        category_list = []
        for item in queryset:
            output = {
                'pop_id': item.pop_id,
                'category': item.category,
                'popularity_count': item.popularity_count
            }
            category_list.append(output)
         
        return self.build_response('Success', category_list, status.HTTP_200_OK)
        
    def featured_products(self):
        serializer_class = ProductSerializer
        queryset = Product.objects.filter(feautured=True)
        
        featured_list = []
        for item in queryset:
            output = {
                'pid': item.pid,
                'title': item.title,
                'description': item.description,
                'price': item.price
            }
            featured_list.append(output)
            
        return self.build_response("Success", featured_list, status.HTTP_200_OK)
        
    def popular_reviews(self):
        serializer_class = ProductReviewSerialzer
        queryset = ProductReview.objects.all().order_by('created_at')

        reviews_list = []
        for item in queryset:
            reviews = {
                "rev_id": item.rev_id,
                "title": item.review_title,
                "review_text": item.review_text,
                "rating": item.review_rating
            }
            reviews_list.append(reviews)
            
        return self.build_response("Success", reviews_list, status.HTTP_200_OK)
        
        
    def special_offers(self):
        pass
        
    def trending_products(self):
        pass

# Responsible for getting all products in the database - Renders products in the catalogue page
class ProductCatalogue(RequestValidation):
    def get(self, request):
        serializer_class = ProductSerializer
        queryset = Product.objects.all()
        
        products_list = []
        for item in queryset:
            product_data = {
                'id': item.id,
                'pid': item.pid,
                'title': item.title,
                'description': item.description,
                'price': item.price,
                'brand_name': item.brand_name,
                'discount': {
                    'dis_id': item.discount.dis_id,
                    'name': item.discount.name,
                    'discount_percent': item.discount.discount_percent,
                    'active': item.discount.active
                },
                'inventory': {
                    'inv_id': item.inventory.inv_id,
                    'quantity': item.inventory.quantity
                },
                'category': {
                    'cat_id': item.category.cat_id,
                    'category_choice': item.category.category_choice
                }
            }
            products_list.append(product_data)
        save_top_categories()
            
        return self.build_response('Success', products_list, status.HTTP_200_OK)
    

# Renders details of a specific product in the product overview page
class GetProductDetail(RequestValidation):
    serializer_class = ProductSerializer

    def get_object(self, pid):
        try:
            product = Product.ojects.get(pid=pid)
            if product is None:
                return self.build_response('Info', f'No Product with id {pk}', status.HTTP_200_OK)
            return product
        except AttributeError:
           return self.build_response('Error', 'Product not Found', status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        required_fields = ['pid']
        self.validate_input_data(required_fields, request.GET)
    
        # Request Data
        requestData = {}
        requestData['pid'] = request.GET.get('pid')
        print(requestData)

        product = self.get_object(requestData.get('pid'))
        serializer = self.serializer_class(product, many=False)
        return self.build_response('Success', serializer.data, status.HTTP_200_OK)
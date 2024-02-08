from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import ProductSerializer, PopularProductSerializer
from .models import Product, PopularProduct

from knox.auth import TokenAuthentication

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
        _methods = {
            'popular_categories': self.popular_categories(),
            'featured': self.featured_products(),
            'reviews': self.popular_reviews(),
            'specials': self.special_offers(),
            'trending': self.trending_products()
        }
        return self.featured_products()

    def popular_categories(self):
        serializer_class = PopularProductSerializer
        queryset = PopularProduct.objects.all()
        
        output = {}
        for item in queryset:
            output['pop_id'] = item.pop_id
            output['category'] = item.category
            output['popularity_count'] = item.popularity_count
         
        return self.build_response('Success', output, status.HTTP_200_OK)
        
    def featured_products(self):
        serializer_class = ProductSerializer
        queryset = Product.objects.filter(feautured=True)
        
        featured_product = {}
        for item in queryset:
            featured_product['pid'] = item.pid
            featured_product['title'] = item.title
            featured_product['description'] = item.description
            featured_product['price'] = item.price
            
        return self.build_response("Success", featured_product, status.HTTP_200_OK)
        
    def popular_reviews(self):
        pass
        
    def special_offers(self):
        pass
        
    def trending_products(self):
        pass

# Responsible for getting all products in the database - Renders products in the catalogue page
class ProductCatalogue(RequestValidation):
    def get(self, request):
        serializer_class = ProductSerializer
        queryset = Product.objects.all()
        
        products = {}
        for item in queryset:
            products['pid'] = item.pid
            products['title'] = item.title
            products['description'] = item.description
            products['price'] = item.price
            products['title'] = item.brand_name
            products['discount'] = [item.discount.dis_id, item.discount.name, item.discount.discount_percent, item.discount.active]
            products['inventory'] = [item.inventory.inv_id, item.inventory.quantity]
            products['category'] = [item.category.cat_id, item.category.category_choice]
            
        return self.build_response('Success', products, status.HTTP_200_OK)
    

# Renders details of a specific product in the product overview page
class GetProductDetail(RequestValidation):
    serializer_class = ProductSerializer

    def get_object(self, pk):
        try:
            product = Product.ojects.get(pid=pk)
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

        product = self.get_object(requestData.get('pid'))
        serializer = self.serializer_class(product, many=False)
        return self.build_response('Success', serializer.data, status.HTTP_200_OK)
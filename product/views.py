from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ValidationError

from .serializer import *
from .models import *
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
    allowed_methods = ['GET']
    
    def get(self, request):
        save_top_categories()
        
        categories = self.popular_categories()
        featured = self.featured_products()
        reviews = self.popular_reviews()
        
        result = {
            "popular_categories": categories,
            "featured_products": featured,
            "popular_reviews": reviews,
        }
        
        return self.build_response("Success", result, status.HTTP_200_OK)

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
         
        return category_list
        
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
            
        return featured_list
        
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
            
        return reviews_list
        
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
            product = Product.objects.get(pid=pid)
            if product is None:
                return self.build_response('Info', f'No Product with id {pid}', status.HTTP_200_OK)
            return product
        except AttributeError:
           return self.build_response('Error', 'Product not Found', status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pid, *args, **kwargs):
        
        try:
            product = self.get_object(pid)
            serializer = self.serializer_class(product)
            return self.build_response('Success', serializer.data, status.HTTP_200_OK)
        except Http404 as e:
            return self.build_response("Error", str(e), status.HTTP_404_NOT_FOUND)
        

#brand views
class BrandView(APIView):
    def get(self,request):
        queryset = Brand.objects.all()
        serializer = BrandSerializer(queryset, many=True)
        data ={
            'message': 'Successfully Got All Brand',
            'result': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):

        # get all data
        serializer = BrandSerializer(data = request.data)
        input_data = request.data
        
        new_data = Brand.objects.create(**input_data)

        try:
            # check if data is valid
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({
                'message': 'Brand added succesfully',
                'result' : serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            # handle validation errors

            return Response({
                'message': "An error occured while adding the brand",
                'errors': str(e)

            },status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        return Response('Added Brand', status=status.HTTP_201_CREATED)


#  categories

class CategoryView(APIView):
    def get(self,request):
        
       
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        # import ipdb
        # ipdb.set_trace()
        data ={
            'message': 'Successfully Got All Brand',
            'result': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post (self, request):
        serializer = CategorySerializer(data = request.data)
        input_data = request.data

        new_categories = Category.objects.create(**input_data)

        try: 
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response(
                {
                    'message' : 'Category created succesfully',
                    'result': serializer.data
                }, status = status.HTTP_201_CREATED)
        except ValidationError as e:
            # handle validation errors

            return Response({
                'message': "an error occured while adding categories",
                'errors':str(e)

            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response ('Added Category', status = status.HTTP_201_CREATED)
          
        

class InventoryView(APIView):

    def get(self, request):
        queryset = Inventory.objects.all()
        serializer = InventorySerializer(queryset, many = True)

        data = {
            'message' : 'Inventory created succesfully',
            'result' : serializer.data

        }

        return Response(data, status=status.HTTP_200_OK)
    
    def post (self, request):
        
        #retrieve data from serializer

        serializer = InventorySerializer(data = request.data)
        input_data = request.data

        new_inventory = Inventory.objects.create(**input_data)

        try: 
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({
                'message' : 'Inventory created succesfully',
                'result' : serializer.data
            }, status = status.HTTP_201_CREATED)
        
        except ValidationError as e:

            return Response({
                'message' : 'Error occured while adding inventorys',
                'errors' : str(e)
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response ('added category', status=status.HTTP_201_CREATED)


class ProductOrderView(APIView):
    def get(self, request):
        queryset = ProductOrders.objects.all()
        serializer = ProductOrdersSerializer(queryset, many = True)

        data = {
            'message' : 'Orders created succesfully',
            'result' :  'serializer.data'
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    def post (self, request):
        # get data from the serializer  
        
        serializer = ProductOrdersSerializer(data = request.data)
        input_data = request.data

        input_data = ProductOrders.objects.create(**input_data)
        try:
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({
         
             'message' : 'orders created successfuly',
             'result' :serializer.data
         }, status = status.HTTP_201_CREATE)
        
        except ValidationError as e:

            return Response({
                'message' : 'An error occured when adding orders',
                "error" : str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderedItemsView(APIView):
    def post(self,request):
        pass
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ValidationError

from .serializer import *
from .models import *
from knox.auth import TokenAuthentication

from utils.utils import save_top_categories
from django.shortcuts import get_object_or_404

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

            },status = status.HTTP_400_BAD_REQUEST)
        

        return Response('Added Brand', status=status.HTTP_201_CREATED)


#  categories

class CategoryView(APIView):
    def get(self, request, category_id=None):
        if category_id:
            # Get one category if category_id is provided
            category = get_object_or_404(Category,  category_id)
            category_data = {
                'id': category.category_id,
                'name': category.name,
                'description': category.description
            }
            return Response({
                'message': 'Got one category',
                'result': category_data
            }, status=status.HTTP_200_OK)
        else:
            # Get all categories if category_id is not provided
            queryset = Category.objects.all()
            serializer = CategorySerializer(queryset, many=True)
            data = {
                'message': 'Successfully got all categories',
                'result': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        input_data = request.data

        new_inventory = Category.objects.create(**input_data)

        try:
            serializer.is_valid(raise_exception=True)  # Validate before creating the category
            serializer.save()  # Save new category
            return Response(
                {
                    'message': 'Category created successfully',
                    'result': serializer.data
                }, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            # Handle validation errors
            return Response({
                'message': "An error occurred while adding category",
                'errors': serializer.errors  # Provide detailed validation errors
            }, status=status.HTTP_400_BAD_REQUEST)



class InventoryView(APIView):

    def get(self, request):
        queryset = Inventory.objects.all()
        serializer = InventorySerializer(queryset, many = True)

        data = {
            'message' : 'succesfully got all invntories',
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
            }, status = status.HTTP_400_BAD_REQUEST)
        
        return Response ('added category', status=status.HTTP_201_CREATED)


class ProductOrderView(APIView):
    def get(self, request):
        queryset = ProductOrders.objects.all()
        serializer = ProductOrdersSerializer(queryset, many = True)

        data = {
            'message' : 'Orders created succesfully',
            'result' : serializer.data
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    def post (self, request):
        # get data from the serializer  
        
        serializer = ProductOrdersSerializer(data = request.data)
        input_data = request.data

        new_orders  = ProductOrders.objects.create(**input_data)
        try:
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({
         
             'message' : 'orders created successfuly',
             'result' :serializer.data
         }, status = status.HTTP_201_CREATED)
        
        except ValidationError as e:

            return Response({
                'message' : 'An error occured when adding orders',
                "error" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ProductReviewView(APIView):
    def get(self,request):
        queryset = ProductReview.objects.all()
        serializer = ProductReviewSerialzer(queryset, many = True)

        data = {
            'message' : 'succesfully got all reviews',
            'result' : serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
        
    def post(self, request):

        serializer  = ProductReviewSerialzer(data = request.data)
        input_data = request.data
        
        reviews = ProductReview.object.create(**input_data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message': 'review added succesfully',
                'result' : serializer.data
            }, status= status.HTTP_201_created)
        except ValidationError as e:
            return Response(
                {
                    'message' : 'Error occured while adding reviews',
                    'errors' : str(e)

                }, status=status.HTTP_400_BAD_REQUEST
            )
        
class ProductTagView(APIView):
    def get(self, request):
        queryset = ProductTag.objects.all()
        serializer = ProductTagSerializer(queryset, many = True)

        data = {
            'message': 'succesfully got all tags',
            'result' : serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductTagSerializer(data = request.data)
        input_data = request.data
        
        tags = ProductTag.objects.create(**input_data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message' : 'tag added succesfully',
                'result' : serializer.data

            },status=status.HTTP_201_CREATED)
        
        except ValidationError as e:

            return Response(
                {
                    'message' : 'Error occured while adding tags',
                    'errors' : str(e)

                }, status=status.HTTP_400_BAD_REQUEST
            )

class ProductTagMappingView(APIView):
    def get(self, request):
        queryset = ProductTagMapping.objects.all()
        serializer = ProductTagMappingSerializer(queryset, many = True)

        data = {
            'message': 'succesfully got all tags',
            'result' : serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductTagMappingSerializer(data = request.data)
        input_data = request.data
        
        tags = ProductTag.objects.create(**input_data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message' : 'tag added succesfully',
                'result' : serializer.data

            },status=status.HTTP_201_CREATED)
        
        except ValidationError as e:

            return Response(
                {
                    'message' : 'Error occured while creating mappings',
                    'errors' : str(e)

                }, status=status.HTTP_400_BAD_REQUEST
            )

class Wishlistview(APIView):
    def get(self, request):
        queryset = Wishlist.objects.all()
        serializer = WishlistSeializer(queryset, many = True)

        data = {
        'message' : 'Wishlist retrieved succesfully',
        'result' : serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = WishlistSeializer(data = request.data)
        input_data = request.data

        new_wishlist = Wishlist.objects.create(**input_data)

        "error handling"
        try: 
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message' : 'Wishlist created succesfully',
                'result': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({
                'message': 'an error occured while adding wishlist',
                'error' : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ProductFeatureView(APIView):
    def get (self, request):
        queryset = ProductFeature.objects.all()
        serializer =  ProductFeaturesSerializer(queryset, many = True)
        data = {
            'message': 'succesfully got all features ',
            'result' : serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProductFeaturesSerializer(data = request.data)
        input_data = request.data

        new_features = ProductFeature.objects.create(**input_data)

        "error handling"

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message' : "Product features created succesfully",
                'result' : serializer.data
            }, status = status.HTTP_201_CREATED)
        except ValidationError as e:
             return Response({
                 'message' : 'An error occured while adding Product Features',
                 'error' : str(e)
             }, status=status.HTTP_400_BAD_REQUEST)


class ProductFeatureMappingView(APIView):
    def get(self, request):
        queryset = ProductFeatureMappings.objects.all()
        serializer = ProductFeatureMappingSerializer(queryset, many =True)

        data = {
            'message' : 'succesfully got feature_mappings',
            'result' : serializer.data
        }

        return Response(data, status = status. HTTP_200_OK)
    
    def post (self, request):
        serializer = ProductFeatureMappingSerializer(data = request.data)
        input_data = request.data

        new_mappings = ProductFeatureMappings.objects.create(**input_data)

        'validation errors handling'
        try:
            serializer.is_valid(raise_exception = True)
            serializer.save()

            return Response({
                'message' : 'Featuremappings created succesfully',
                'result' : serializer.data
            }, status= status.HTTP_201_CREATED)
        
        except ValidationError as e:
             return Response({
                 'message' : 'an error occured while adding feature_mappings',
                 'error' :str(e)
             }, status= status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import ProductSerializer
from .models import Product
 
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

# Base Class for unified Responses and Custom Validation Messages
class RequestValidation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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

# Responsible for getting all products in the database - Renders products in the catalogue page
class ProductCatalogue(RequestValidation):
    serializer_class = ProductSerializer
    queryset = Product.objects

    def get(self, request):
        """
            # Displaying all products
            displayed:  product image,
                        product title,
                        product price, 
                        product rating
        """
        products = self.queryset.all()
        serializer = self.serializer_class(products, many=True)
        return self.build_response('Success', serializer.data, status.HTTP_200_OK)
    
class ProductCreateView(RequestValidation):
    def post(self, request, *args, **kwargs):
       serializer = self.serializer_class(data=request.POST)
       if serializer.is_valid():
          serializer.save()
          return self.build_response('Created Successfully', serializer.data, status.HTTP_201_CREATED)
       return self.build_response('Error', serializer.errors, status.HTTP_400_BAD_REQUEST)

# Renders details of a specific product in the product overview page
class ProductOverview(RequestValidation):
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
        """
            Display the details of the specific product
            displayed:  product full image,
                        product inventory numbers,
                        product title,
                        product short description,
                        product rating,
                        product price,
                        product style/storage,
                        product color
                        product additional images,
                        product full description,
                        product details/specs,
                        product reviews:    product rating,
                                            product user reviews:   user name,
                                                                    user profile image,
                                                                    user text review,
                                                                    user product images

        """
        required_fields = ['product_id'] 
        self.validate_input_data(required_fields, request.GET)
    
        # Request Data
        requestData = {}
        requestData['product_id'] = request.GET.get('product_id')

        product = self.get_object(requestData.get('product_id'))
        serializer = self.serializer_class(product, many=False)
        return self.build_response('Success', serializer.data, status.HTTP_200_OK)
    
    def put(self, request):

        required_fields = ['product_id', 'title', 'description', 'price'] 
        self.validate_input_data(required_fields, request.GET)
    
        # Request Data
        requestData = {}
        requestData['pid'] = request.GET.get('product_id')
        requestData['title'] = request.GET.get('title')
        requestData['description'] = request.GET.get('description')
        requestData['price'] = request.GET.get('price')

        product = self.get_object(requestData.get('product_id'))

        serializer = ProductSerializer(product, data=requestData)
        if serializer.is_valid():
            serializer.save()
            return self.build_response('Success', serializer.data, status.HTTP_200_OK)
        return self.build_response('Error', serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        required_fields = ['product_id'] 
        self.validate_input_data(required_fields, request.GET)
    
        # Request Data
        requestData = {}
        requestData['pid'] = request.GET.get('product_id')

        product = self.get_object(requestData.get('product_id'))

        product.delete()
        return self.build_response('Success', 'Deleted Product', status.HTTP_204_NO_CONTENT)
    

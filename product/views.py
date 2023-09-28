from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer
from .models import Product


# Responsible for getting all products in the database
# Renders products in the catalogue page
class ProductCatalogue(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        """
            # Displaying all products
            displayed:  product image,
                        product title,
                        product price, 
                        product rating
        """
        try:
            output = [
                {
                    'pid': output.pid,
                    'title': output.title,
                    'description': output.description,
                    'price': output.price,
                } for output in Product.objects.all()
            ]
            return Response(
                output,
                status=status.HTTP_200_OK
            )
        except Exception as error:
           return Response(
               {
                   'message': error
               },
               status=status.HTTP_400_BAD_REQUEST
           )

# Renders details of a specific product
# in the product overview page
class ProductOverview(APIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

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
        pass

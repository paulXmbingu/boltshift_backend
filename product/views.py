from rest_framework.views import APIView
from rest_framework.response import Response
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
        pass

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

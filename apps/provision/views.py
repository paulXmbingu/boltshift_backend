from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from apps.provision.models import ShoppingSession, CartItem
from .serializer import ShoppingSessionSerializer, CartItemSerializer
import json

# Base Class for unified Responses and Custom Validation Messages
class RequestValidation(APIView):
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
    
class ShoppingSessionView(RequestValidation):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
            Get Current Shopping Session
        """
        current_user = request.user.id

        try:
        
            shop_sesh = ShoppingSession.objects.filter(user_id = current_user).first()

            # create a new shopping session if not already
            if shop_sesh is None:
                data = request.data
                data['user_id'] = current_user
                data['total'] = 0

                new_session = ShoppingSession.objects.create(**data)
                serializer = ShoppingSessionSerializer(new_session)
                return self.build_response("Success", serializer.data,  status.HTTP_200_OK)
            
            # Serialize the existing session
            serializer_data = serialize('json', [shop_sesh])
            json_serializable_data = json.loads(serializer_data)[0]['fields']

            serializer = ShoppingSessionSerializer(data=json_serializable_data)
            serializer.is_valid()

            return self.build_response("Success", serializer.data, status.HTTP_200_OK)

        except Exception as e:
            return self.build_response("Error", {str(e)}, status.HTTP_400_BAD_REQUEST)        

class CartSessionView(RequestValidation):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def common(self, **kwargs):
        shopping_sesh = ShoppingSession.objects.filter(sess_id=kwargs.get('shopping_sesh_id'), user_id=kwargs.get('current_user')).first()

        if shopping_sesh is None:
            return self.build_response("Error", "Shopping Session ID not Found. Try again", status.HTTP_400_BAD_REQUEST)
        
        return shopping_sesh

    def get(self, request):
        try:
            current_user = request.user.id
            shopping_sesh_id = request.GET.get('shopping_sesh')

            shopping_sesh = self.common(shopping_sesh_id=shopping_sesh_id, current_user=current_user)

            # get cart items based on shipping session
            cartItems = CartItem.objects.filter(session_id=shopping_sesh.id)
            
            serializer = CartItemSerializer(cartItems, many=True)

            return self.build_response("Success", serializer.data, status.HTTP_200_OK)
        
        except Exception as e:
            return self.build_response("Error", {str(e)}, status.HTTP_400_BAD_REQUEST) 

    def post(self, request):
        try:
            current_user = request.user.id

            data = request.data

            data["shopping_sesh_id"] = request.POST.get('shopping_sesh')
            data["product_id"] = request.POST.get('product_id')

            shopping_sesh = self.common(shopping_sesh_id=data.get("shopping_sesh_id"), current_user=current_user)

            data["session_id"] = shopping_sesh.get('id')
            # create a new cart item
            serializer = CartItemSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return self.build_response("Success", serializer.data, status.HTTP_200_OK)

        except Exception as e:
            return self.build_response("Error", {str(e)}, status.HTTP_400_BAD_REQUEST)
    
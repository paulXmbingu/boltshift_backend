from django.shortcuts import render
from .serializer import Vendor
from rest_framework import generics
from .serializer import VendorSerializer
from rest_framework.response import Response


class VendorAPI(generics.ListCreateAPIView):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    def get(self, request):
        output = [
            {
                'id': output.id,
                "uuid": output.vend_id,
                'username': output.vendor_name,
                'password': output.password,
                'email': output.email,
                'description': output.description,
                'rating': output.rating
            } for output in Vendor.objects.all()
        ]
        # status code
        return Response(output)
    
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
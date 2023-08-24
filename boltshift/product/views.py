from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# the catalogue page
def ProductCatalogue(request):
    message = "Welcome User"
    return HttpResponse(message)


# the product overview
def ProductOverview(request):
    pass

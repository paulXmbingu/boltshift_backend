from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Customer, UserCardInformation
from django.contrib.auth import login, authenticate
from rest_framework import generics
from .customer_serializer import CustomerSerializer

# API handling
class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# home page
def HomePage(request):
    return redirect('product_catalogue')


# user registration
def UserRegistration(request):
    if request.method == "POST":
        customer_first_name = request.POST[""]
        customer_last_name = request.POST[""]
        customer_email = request.POST[""]
        customer_phone_number = request.POST[""]
        customer_password = request.POST[""]
        customer_terms = request.POST[""]

        customer_full_name = " ".join([customer_first_name, customer_last_name])

        newCustomer = Customer.objects.create(customer_full_name, customer_email,customer_phone_number, customer_password, customer_terms)
        newCustomer.customer_name = customer_full_name
        newCustomer.email = customer_email
        newCustomer.phone_number = customer_phone_number
        newCustomer.password = customer_password
        newCustomer.terms_conditions = customer_terms

        newCustomer.save()

        messages.success(request, "Account Successfully Created")

        return redirect("")

# user login
def UserLogin(request):
    if request.method == "POST":
        email_phone = request.POST[""]
        password = request.POST[""]

        user = authenticate()

        if user is not None:
            login(user)
        else:
            pass

# user logout
def UserLogout(request):
    pass


# user password reset
def UserPasswordReset(request):
    if request.method == "POST":
        pass


# user account settings
def UserAccountSettings(request):
    pass


# user profile
def UserProfile(request):
    pass

# user shopping cart
def UserShoppingCart(request):
    # list out all the products in the currentuser.cart
    pass

# user wishlist
def UserWishlist(request):
    # return all products in the current_user.wishlist
    pass

# user product checkout
def UserProductCheckout(request):
    pass

# user product orders
def UserProductOrders(request):
    pass

# user payment methods
# get user card information from database
def UserPaymentMethod(request):
    pass


# user vouchers
def UserVouchers(request):
    pass


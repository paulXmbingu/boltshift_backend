from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.response import Response
from .models import CustomUser
from .serializer import SerializeCustomer
from django.views.decorators.csrf import csrf_protect


def index(request):
    return HttpResponse("<h2>Welcome to <b><i>Boltshift E-commerce</i></b></h2>")

# API serializer wrapper
class CustomerAPI(viewsets.ModelViewSet):
    serializer_class = SerializeCustomer
    queryset = CustomUser.objects.all()

    def get(self, request):
        output = [
            {
                'id': output.id,
                "uuid": output.cid,
                'username': output.username,
                'first name': output.first_name,
                'last name': output.last_name,
                'password': output.password,
                'active status': output.is_active,
                'email': output.email,
            } for output in CustomUser.objects.all()
        ]
        # status code
        return Response(output)
    
    def post(self, request):
        serializer = SerializeCustomer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class CustomerRegistrationAPI(viewsets.ModelViewSet):
    def validate(self, data):
        if data['password1'] != data['password2']:
            pass

class CustomerLoginAPI(viewsets.ModelViewSet):
    user = CustomUser.objects.all()
    
    def validate(self, data):
        pass


@csrf_protect
def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST or None)

        # form validation
        if form.is_valid():

            # form data cleaning
            username = form.cleaned_data['username']

            # sending a success message
            messages.success(request, "Account Created Successfully!")

            #saving data
            form.save()

            # user credentials authentication
            new_user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            # user logining in
            login(request, new_user)

            # redirecting to login page
            return redirect("login")
        
    # if request is GET
    else:
        form = RegistrationForm()
        return HttpResponse("Ready to sign up")
        

@csrf_protect
def login(request):
    # if user is already logged in
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            # quering users from database
            user = CustomUser.objects.all(email=email)
        except Exception as error:
            print(f"Error Encountered: {error}")

        # logging in user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully")
            redirect("home")
    
    return HttpResponse("Ready to login in")

def sign_out(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("home")


def delete_account(request, id):
    if request.method == 'POST':
        # deleting the user
        request.user.delete()

        # logout user after deletion
        #logout(request)

        # redirect to home page
        return redirect('home')
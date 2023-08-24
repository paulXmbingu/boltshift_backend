from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# user sign up registration form
class UserRegistrationForm(UserCreationForm):
    preferred_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('preferred_name', 'email', 'password')
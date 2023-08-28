from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
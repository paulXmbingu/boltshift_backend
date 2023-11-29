# contains the @override_method that overrides the in-built
# authenticate method to create our own

from django.contrib.auth.backends import ModelBackend
from .models import Customer

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Customer.objects.get(email=username)

            if user.check_password(password):
                return user
            else:
                return None  # Password is incorrect
        except Customer.DoesNotExist:
            return None  # User with this email does not exist

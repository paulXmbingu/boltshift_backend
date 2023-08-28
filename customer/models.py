from django.db import models
from django.contrib.auth.models import AbstractUser

# customiing our user
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __repr__(self):
        return f"{self.username}, {self.email}"
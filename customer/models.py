from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits

# customiing our user
class CustomUser(AbstractUser):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="user-", alphabet=hexdigits)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __repr__(self):
        return f"{self.username}, {self.email}"
    
    class Meta:
        # rename the class incase of multiple users
        verbose_name_plural = "Customers"
from django.db import models
from customer.models import CustomUser
from string import hexdigits
from shortuuid.django_fields import ShortUUIDField

"""
# Creates a directory for each user
#
"""
def user_directory_path(instance, filename):
    return f"vendor_{instance.user.id}/{filename}"


class Vendor(models.Model):
    vend_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="vend-", alphabet=hexdigits)
    vendor_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    registration_date = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=100, blank=True, default="Cool")
    rating = models.CharField(max_length=100, blank=True, default="Cool")
    
    warranty_period = models.PositiveIntegerField()
    response_time = models.CharField(max_length=100, blank=True, default="Cool")
    shipping_time = models.CharField(max_length=100, blank=True, default="Cool")

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def __repr__(self) -> str:
        return self.vendor_name
    

class Address(models.Model):
    phone_number = models.CharField(max_length=20, blank=True, default="Cool")
    address = models.TextField()

    class Meta:
        verbose_name_plural = "Address"
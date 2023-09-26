from django.db import models
from customer.models import CustomUser
from product.models import Product
from string import hexdigits
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

"""
# Creates a directory directory for each user
# the folder name will be in the format: vendor_1/cat.jpg
"""
def user_directory_path(instance, filename):
    return f"{instance.cid}/{filename}"


# the sellers
class Vendor(AbstractUser):
    vend_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="vend-", alphabet=hexdigits)
    vendor_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)

    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=100, blank=True, default="Cool")
    
    warranty_period = models.PositiveIntegerField(default=0)
    response_time = models.CharField(max_length=100, blank=True, default="Cool")
    shipping_time = models.CharField(max_length=100, blank=True, default="Cool")

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)

    # a vendor will have several products at the store
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def image_category(self):
        return mark_safe('<img src="%s" width=50 heigh=50 />', (self.image.url))

    class Meta:
        verbose_name_plural = "Vendors"

    # avoiding field clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='seller_set'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='seller_set'
    )

    def __repr__(self) -> str:
        return f"{self.vendor_name}, {self.email}"
    

class Address(models.Model):
    phone_number = models.CharField(max_length=20, blank=True, default="Cool")
    address = models.TextField()

    class Meta:
        verbose_name_plural = "Address"
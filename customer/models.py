from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits
from django.utils.html import mark_safe
from vendors.utils import UserAccountMixin

# creates a folder for each admin/customer with the user.cid as the folder name
# to hold each individual user uploaded file
def admin_image_directory(instance, filename):
    return f"{instance.cid}/{filename}"

# customing our user
class CustomUser(UserAccountMixin, AbstractUser):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="user-", alphabet=hexdigits)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    image = models.ImageField(upload_to=admin_image_directory, null=True, blank=True, default=None)

    payment = models.ForeignKey('UserPayment', on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('UserAddress', on_delete=models.SET_NULL, null=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />', (self.image.url))
    
    image_tag.short_description = "Image"
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __repr__(self):
        return self.username
    
    class Meta:
        # rename the class incase of multiple users
        verbose_name_plural = "Customers"

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='buyer_set'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='buyer_set'
    )

# customer payment
class UserPayment(models.Model):
    class Meta:
        verbose_name = "Customer Payment"
        verbose_name_plural = "Customer Payments"
    
    def __repr__(self):
        pass

# customer address
class UserAddress(models.Model):
    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Address"
    
    def __repr__(self):
        pass

# user type
class UserType(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
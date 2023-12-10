from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits
from django.utils.html import mark_safe
from utils.utils import UserAccountMixin

# creates a folder for each admin/customer with the user.cid as the folder name
# to hold each individual user uploaded file
def admin_image_directory(instance, filename):
    return f"{instance.cid}/{filename}"

# customing our user
class Customer(AbstractUser, UserAccountMixin):
    GENDER = {
        ('Male', 'm'),
        ('Female', 'f')
    }
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="user-", alphabet=hexdigits)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to=admin_image_directory, null=True, blank=True, default=None)
    gender = models.CharField(max_length=10, choices=GENDER, default='-------')
    phonenumber_primary = models.PositiveIntegerField(default=0)
    phonenumber_secondary = models.PositiveIntegerField(default=0)
    deleted = models.BooleanField(default=False)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />', (self.image.url))
    
    image_tag.short_description = "Image"
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __repr__(self):
        return self.username
    
    def __str__(self):
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

    def soft_delete(self):
        self.deleted = True
        self.save()

# customer payment
class UserPayment(models.Model):
    pay_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits, prefix='payment-')
    account_number = models.BigIntegerField(default=0)
    provider = models.CharField(max_length=100, default="-----")
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    user_id = models.ForeignKey('Customer', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['account_number', 'provider']

    class Meta:
        verbose_name = "Customer Payment"
        verbose_name_plural = "Customer Payments"
    
    def __repr__(self):
        return self.provider

# customer address
class UserAddress(models.Model):
    addr_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits, prefix='address-')
    streetname = models.TextField(max_length=100, default='None')
    county = models.TextField(max_length=100, default='None')
    city = models.CharField(max_length=50, default="None")
    country = models.CharField(max_length=50, default="None")
    apartment_complex = models.CharField(max_length=500, default="----------")
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    user_id = models.ForeignKey('Customer', on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['streetname', 'county', 'city', 'country', 'phonenumber_primary']

    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Address"
    
    def __repr__(self):
        return self.addr1

# user type
class UserType(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

# user shopping session
class ShoppingSession(models.Model):
    sess_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=hexdigits, prefix="session-")
    total = models.DecimalField(decimal_places=2, max_digits=2)
    user_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Shopping Session"
        verbose_name_plural = "Shopping Sessions"

    def __repr__(self):
        return self.user_id
    
    def __str__(self):
        return self.user_id

    
# Cart Item
class CartItem(models.Model):
    cart_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=hexdigits, prefix="cart-")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    session_id = models.ForeignKey(ShoppingSession, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Cart Items"

    def totalBill(self):
        """
            Return the total amount of all items available in the cart
        """
        pass

    def __repr__(self):
        return self.quantity
    
# customer orders
class ProductOrders(models.Model):
    ORDER_STATUS = {
        ('Pending', 'pending'),
        ('Completed', 'paid'),
        ('Ongoing', 'ongoing'),
        ('Cancelled', 'cancelled')
    }
    ord_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits)
    item_number = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default="-------")
    created_at = models.DateTimeField(default=timezone.now)
    
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Orders"

    def __repr__(self):
        return self.ord_id
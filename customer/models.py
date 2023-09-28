from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits
from django.utils.html import mark_safe
from vendors.utils import UserAccountMixin
from product.models import Product

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
    pay_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits, prefix='payment-')
    account_number = models.PositiveIntegerField(default=0)
    provider = models.CharField(max_length=100, default="-----")
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['account_number', 'provider']

    class Meta:
        verbose_name = "Customer Payment"
        verbose_name_plural = "Customer Payments"
    
    def __repr__(self):
        return self.provider

# customer address
class UserAddress(models.Model):
    addr_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits, prefix='address-')
    addr1 = models.TextField(max_length=100, default='None')
    addr2 = models.TextField(max_length=100, default='None')
    city = models.CharField(max_length=50, default="None")
    country = models.CharField(max_length=50, default="None")
    phonenumber_primary = models.PositiveIntegerField(default=0)
    phonenumber_secondary = models.PositiveIntegerField(default=0)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['addr1', 'city', 'country', 'phonenumber_primary']

    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Address"
    
    def __repr__(self):
        return self.addr1

# user type
class UserType(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

# user product review 
# N/B: a review MUST be tied to the corresponding product, also the user
class ProductReview(models.Model):
    RATINGS = {
        ('⭐⭐⭐⭐⭐', 5),
        ('⭐⭐⭐⭐', 4),
        ('⭐⭐⭐', 3),
        ('⭐⭐', 2),
        ('⭐', 1),
    }
    rev_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='review-', alphabet=hexdigits)
    review_title = models.CharField(max_length=50, default='Great Product')
    review_screenshots = models.ImageField(upload_to=admin_image_directory, null=True, blank=True, default=None)
    review_text = models.CharField(max_length=1000, default='I love the product')
    review_rating = models.CharField(max_length=50, choices=RATINGS, default='------')
    created_at = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def review_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />', (self.review_screenshots.url))
    
    review_tag.short_description = "Image"

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __repr__(self):
        return self.review_title
    
# user shopping session
class ShoppingSession(models.Model):
    sess_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=hexdigits, prefix="session-")
    total = models.DecimalField(decimal_places=2, max_digits=2)
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Shopping Session"
        verbose_name_plural = "Shopping Sessions"

    def __repr__(self):
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
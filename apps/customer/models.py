from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
import string
from django.utils.html import mark_safe
from utils.utils import UserAccountMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def customer_image_upload_directory(instance, filename):
    return f"{instance.__class__.__name__}/{instance.cid}/{filename}"
    
    
def validate_expiry_date(value):
    pass


class Customer(AbstractUser, UserAccountMixin):
    GENDER = {
        ('Male', 'Male'),
        ('Female', 'Female'),
    }
    
    cid = ShortUUIDField(verbose_name='Customer ID', unique=True, length=10, max_length=15, prefix="Cust-", alphabet=string.digits)
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    gender = models.CharField(max_length=10, choices=GENDER, default='Select Gender', verbose_name='Gender')
    username = models.CharField(max_length=20, unique=True, verbose_name='User Name')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    phonenumber_primary = models.CharField(verbose_name='Primary Phone Number', max_length=20)
    image = models.ImageField(upload_to=customer_image_upload_directory, null=True, blank=True, default=None, verbose_name='Profile Photo')
    deleted = models.BooleanField(verbose_name='Soft Delete', default=False)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" height="100" />' % (self.image.url))
    
    image_tag.short_description = "Current Profile Photo"
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __repr__(self):
        return self.username
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Customers"

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('Groups'),
        blank=True,
        related_name='buyer_set'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('User Permissions'),
        blank=True,
        related_name='buyer_set'
    )

    def soft_delete(self):
        self.deleted = True
        self.save()


class UserCardInformation(models.Model):
    CARD_TYPE = {
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
        ('American Express', 'express'),
        ('Discover', 'Discover'),
        ('UnionPay', 'Unionpay')
    }
    
    pay_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix='PayID-')
    debit_credit_card_number = models.BigIntegerField(default=0)
    card_provider = models.CharField(max_length=50, default="Select your card type", choices=CARD_TYPE)
    card_expiry_date = models.DateField()
    card_security_code = models.IntegerField(default=0)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    #card_billing_address = models.ForeignKey('UserAddress', on_delete=models.SET_NULL, null=True)

    REQUIRED_FIELDS = ['debit_credit_card_number', 'card_provider', 'card_expiry_date', 'card_security_code']

    class Meta:
        verbose_name = "Customer Card Information"
        verbose_name_plural = "Customer Card Information"
    
    def __repr__(self):
        return "{} {} {}".format(self.card_provider, self.user_id, self.pay_id)
    
    def __str__(self):
        return "{} {} {}".format(self.card_provider, self.user_id, self.pay_id)
    

class UserAddress(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    addr_id = ShortUUIDField(verbose_name='Address ID', unique=True, length=10, max_length=15, alphabet=string.digits, prefix='AddressID-')
    streetname = models.CharField(verbose_name='Street Name', max_length=100)
    county = models.CharField(verbose_name='County', max_length=100)
    city = models.CharField(verbose_name='City', max_length=50)
    country = models.CharField(verbose_name='Country', max_length=50)
    apartment_complex = models.CharField(verbose_name='Apartment', max_length=500)
    # updated_at = models.DateTimeField(default=timezone.now, verbose_name='Updated')
    # created_at = models.DateTimeField(default=timezone.now, verbose_name='Created')
    

    REQUIRED_FIELDS = ['streetname', 'county', 'city', 'country', 'phonenumber_primary']

    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Address"
    
    def __repr__(self):
        return self.addr1

class UserType(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits
from django.utils.html import mark_safe
from vendors.models import Vendor
from customer.models import CustomUser

RATING = (
    (0, '00000'),
    (1, '10000'),
    (2, '11000'),
    (3, '11100'),
    (4, '11110'),
    (5, '11111')
)


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="product-", alphabet=hexdigits)
    title = models.CharField(max_length=100)
    description = models.TextField()
    stock_quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    specifications = models.TextField(null=True, blank=True)


    # foreign keys
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)


class Category(models.Model):
    cat_id = ShortUUIDField(unique=True, length=10, alphabet=hexdigits)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category")


    def image_category(self):
        return mark_safe('<img src="%s" width=50 heigh=50 />', (self.image.url))

    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return self.title

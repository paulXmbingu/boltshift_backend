from django.db import models
import os

# create the folder images if it does not exist
if not os.path.exists("product/images"):
    os.makedirs("product/images")

# product models
"""
# Product specs:
title, price, category, image, description, color, style, stocks left, star review
"""
class Product(models.Model):
    STYLE_CHOICES = (
        ('DE', 'Designer Edition'),
        ('LE', 'Limited Edition'),
        ('FE', 'Factory Edition')
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    stock = models.PositiveBigIntegerField(default=0)
    style = models.CharField(max_length=2, choices=STYLE_CHOICES, default='DE')

    # saving image to product/image
    image = models.ImageField(upload_to='product/images')

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    details = models.ForeignKey('Details', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


# product category
class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


# product details
class Details(models.Model):
    dimensions = models.CharField(max_length=50)
    model_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    asin = models.CharField(max_length=50, unique=True)
    country_of_origin = models.CharField(max_length=50)
    seller_rank = models.CharField(max_length=100)    
from django.db import models
from product.models import Product
import os

if not os.path.exists("user/images/"):
    os.makedirs("user/images")


# user model
class Customer(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('PNS', 'Prefer Not to Say')
    )

    customer_name = models.CharField(max_length=50)
    terms_conditions = models.BooleanField(default=False)
    gender = models.CharField(max_length=3, choices=GENDER, default='PNS')
    date_of_birth = models.DateField(default=models.DateField(auto_now_add=True))
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    password = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(upload_to="user/images")

    address = models.ForeignKey('UserAddress', on_delete=models.SET_NULL, null=True, blank=True)
    bank_card = models.ForeignKey('UserCardInformation', on_delete=models.SET_NULL, null=True, blank=True)
    product_review = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True, blank=True)
    shipping = models.ForeignKey('ShippingDetails', on_delete=models.SET_NULL, null=True, blank=True)

    # wishlist
    wishlist = models.ManyToManyField(Product, through='WishListItem')

    def __repr__(self):
        return self.customer_name


# user address details
class UserAddress(models.Model):
    apartment = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)



# card model
class UserCardInformation(models.Model):
    pass


# user product review
class Review(models.Model):
    pass


# user shipping details
class ShippingDetails(models.Model):
    pass


# user transaction summary
class Transaction(models.Model):
    pass


# user cart bin
class ProductCartBin(models.Model):
    pass

# user orders
# either paid, pending, drafted
class UserProductOrders(models.Model):
    pass


# user wishlist bin
class WishListItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.customer_name}'s Wishlist: {self.product.title}"
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits

from customer.models import CustomUser


# Create your models here.
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
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Orders"

    def __repr__(self):
        return self.ord_id
    
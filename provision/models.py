from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits

from customer.models import CustomUser


# Create your models here.
class ShoppingSession(models.Model):
    sess_id = ShortUUIDField(unique=True, length=10, max_length=22, alphabet=hexdigits, prefix="session-")
    total = models.DecimalField(decimal_places=2, max_digits=9)
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shopping Session"
        verbose_name_plural = "Shopping Sessions"

    def __repr__(self):
        return self.user_id
    
# Cart Item
class CartItem(models.Model):
    cart_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=hexdigits, prefix="cart-")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

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
    
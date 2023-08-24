from django.contrib import admin
from .models import Customer, UserAddress, UserCardInformation, Review, ShippingDetails, Transaction, ProductCartBin, WishListItem

@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'gender',
        'date_of_birth',
        'email',
        'phone_number',
        'address',
        'bank_card',
        'shipping'
    )


@admin.register(UserAddress)
class CustomerAddress(admin.ModelAdmin):
    pass


@admin.register(UserCardInformation)
class CustomerCardInformation(admin.ModelAdmin):
    pass


@admin.register(Review)
class CustomerReview(admin.ModelAdmin):
    pass


@admin.register(ShippingDetails)
class CustomerShippingDetails(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class CustomerTransaction(admin.ModelAdmin):
    pass

@admin.register(ProductCartBin)
class CustomerProductCart(admin.ModelAdmin):
    pass

@admin.register(WishListItem)
class CustomerWishlist(admin.ModelAdmin):
    list_display = ('customer', 'product')
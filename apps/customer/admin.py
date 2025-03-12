from django.contrib import admin
from .models import (Customer, UserAddress,)

@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'cid', 'email', 'phonenumber_primary', 'gender',  ]
    # search_fields = ('email', 'username', 'cid')


@admin.register(UserAddress)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['streetname',]
    search_fields = ['city', 'country',]    
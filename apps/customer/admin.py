from django.contrib import admin
from .models import (Customer, UserAddress,)

@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name']
    search_fields = ('email', 'username', 'cid')
    readonly_fields = ['image_tag']

@admin.register(UserAddress)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['streetname',]
    search_fields = ['city', 'country',]
    readonly_fields = ['streetname', 'county', 'city', 'country']
    
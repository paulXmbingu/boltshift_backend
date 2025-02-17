from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_name', 'email']
    list_filter = ['vendor_name', 'email']
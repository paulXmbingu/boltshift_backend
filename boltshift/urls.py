from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customer.urls')),
    path('product/', include('product.urls')),
    path('vendor/', include('vendors.urls')),
    path('provision/', include('provision.urls')),

    # ckeditor default url image upload route
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

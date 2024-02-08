from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('', include('product.urls')),
    path('vendor/', include('vendors.urls')),
    path('provision/', include('provision.urls')),

    # ckeditor default url image upload route
    path('ckeditor/', include('ckeditor_uploader.urls')),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('customer/', include('apps.customer.urls')),
    path('product/', include('apps.product.urls')),
    path('vendor/', include('apps.vendors.urls')),
    path('provision/', include('apps.provision.urls')),

    # ckeditor default url image upload route
    path('ckeditor/', include('ckeditor_uploader.urls')),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


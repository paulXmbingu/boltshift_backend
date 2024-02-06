from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from customer.views import CatchAllView

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('', include('product.urls')),
    path('vendor/', include('vendors.urls')),
    path('provision/', include('provision.urls')),

    # ckeditor default url image upload route
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # not found urls
    # Catch-all URL pattern using the DRF view
    re_path(r'^.*$', CatchAllView.as_view(), name='catchall')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

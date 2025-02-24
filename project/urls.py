from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(template_name="admin/login.html", redirect_authenticated_user=True, next_page='/admin/'), name='admin_login'),
    path('admin/', admin.site.urls),
    path('customer/', include('apps.customer.urls')),
    path('product/', include('apps.product.urls')),
    path('vendor/', include('apps.vendors.urls')),
    path('provision/', include('apps.provision.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
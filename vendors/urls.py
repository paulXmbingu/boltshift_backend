from django.urls import path, include
from . import views
from rest_framework import routers

register = routers.DefaultRouter()
register.register("", views.VendorRegistration, 'register')

login = routers.DefaultRouter()
login.register("", views.VendorLogin, 'login')

add = routers.DefaultRouter()
add.register("", views.VendorAddProduct, 'add')

mine = routers.DefaultRouter()
mine.register("", views.VendorProductView, 'view')

urlpatterns = [
    path('api/register', include(register.urls)),
    path('api/login', include(login.urls)),
    path('api/add-product', include(add.urls)),
    path('api/vendor-products', include(mine.urls))
]
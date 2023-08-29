from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', views.CustomerAPI, 'user')

urlpatterns = [
    # api handling
    path('api-customer/', include(router.urls)),
    path('', views.index, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.login, name="login"),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('delete-account/', views.delete_account, name='delete-account/<id>')
]
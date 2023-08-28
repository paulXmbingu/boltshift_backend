from django.urls import path
from . import views

urlpatterns = [
    # api handling
    path('api-customer/', views.CustomerAPI.as_view(), name='customer_api'),
    path('', views.index, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.login, name="login"),
    path('sign-out/', views.sign_out, name='sign-out')
]
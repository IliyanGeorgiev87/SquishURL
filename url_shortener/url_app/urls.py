from django.urls import path, include
from . import views

urlpatterns = [
    #* == MISC == *#
    path('homepage/', views.Home, name="home"),
    path('', views.Redirect, name="redirect_home"),
    #* == ACCOUNTS == *#
    path('accounts/register', views.Register, name='register'),
    path('accounts/login', views.Login, name='login'),
    #* == DASHBOARD & APP == *#
    path('dashboard/', views.Dashboard, name='dashboard')
]
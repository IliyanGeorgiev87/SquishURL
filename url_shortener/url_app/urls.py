from django.urls import path, include
from . import views

urlpatterns = [
    #* == MISC == *#
    path('homepage/', views.Home, name="home"),
    path('', views.Redirect, name="redirect_home"),
    #* == ACCOUNTS == *#
    path('accounts/register', views.Register, name='register'),
    path('accounts/login', views.Login, name='login'),
    path('accounts/account/', views.AccountDetail, name='account'),
    path('accounts/account/delete', views.DeleteAccount, name='account_delete'),
    #* == DASHBOARD & APP == *#
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('dashboard/link/create/', views.ShortenUrl, name = "create_url"),
    path('dashboard/link/<int:pk>/delete', views.DeleteURL, name="delete_url")
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('homepage/', views.Home, name="home"),
    path('', views.Redirect, name="redirect_home")
]
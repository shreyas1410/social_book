from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup1', views.signup, name="signup1"),
    path('signin1', views.signin, name="signin1"),
    path('signout', views.signout, name="signout"),
    path('user_list', views.user_list, name="user_list"),
    #path('', views.home, name="home"),
    #path('register', views.register, name="register"),
    #path('login', views.login, name="login"),
]

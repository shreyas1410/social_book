from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('user_list', views.user_list, name="user_list"),
    #path('', views.home, name="home"),
    #path('register', views.register, name="register"),
    #path('login', views.login, name="login"),
]

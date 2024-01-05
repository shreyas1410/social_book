from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup1', views.signup, name="signup1"),
    path('signin1', views.signin, name="signin1"),
    path('signout', views.signout, name="signout"),
    path('user_list', views.user_list, name="user_list"),
    path('upload_files/', views.upload_image, name="upload_files"),
    path('uploaded_files/', views.uploaded_images, name="uploaded_files"),
    #path('', views.home, name="home"),
    #path('register', views.register, name="register"),
    #path('login', views.login, name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

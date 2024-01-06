from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomUserDetailView, GenerateToken
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, UploadedFileViewSet

router = DefaultRouter()
router.register(r'api_users', CustomUserViewSet)
router.register(r'api_uploaded_files', UploadedFileViewSet,basename='uploaded_files')

urlpatterns = [
    path('index', views.home, name="home"),
    path('', views.signup, name="signup1"),
    path('signin1', views.signin, name="signin1"),
    path('signout', views.signout, name="signout"),
    path('user_list', views.user_list, name="user_list"),
    path('upload_files/', views.upload_image, name="upload_files"),
    path('uploaded_files/', views.uploaded_images, name="uploaded_files"),
    path('api/', include(router.urls)),
    path('api1/generate-token', GenerateToken.as_view(), name='generate_token'),
    path('user-details/', CustomUserDetailView.as_view(), name='user-details'),
    

    #path('', views.home, name="home"),
    #path('register', views.register, name="register"),
    #path('login', views.login, name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

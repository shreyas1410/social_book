# serializers.py
from rest_framework import serializers
from .models import CustomUser, UploadedFile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'public_visibility', 'is_active', 'is_staff', 'date_joined']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'user', 'title', 'file', 'price']
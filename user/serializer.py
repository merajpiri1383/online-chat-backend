from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = get_user_model()
        fields = ["phone","is_active","is_manager","username","image"]

class MoreInfoUserSerializer(serializers.ModelSerializer) :
    favorits = UserSerializer(many=True,read_only=True)
    contacts = UserSerializer(many=True,read_only=True)
    class Meta :
        model = get_user_model()
        fields = ["phone","is_active","is_manager","username","image","favorits","contacts"]
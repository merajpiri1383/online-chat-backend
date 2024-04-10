from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = get_user_model()
        fields = ["id","phone","is_active","is_manager"]

class MoreInfoUserSerializer(serializers.ModelSerializer) :
    favorits = UserSerializer(many=True,read_only=True)
    contacts = UserSerializer(many=True,read_only=True)
    blacklist = UserSerializer(many=True,read_only=True)
    class Meta :
        model = get_user_model()
        fields = ["id","phone","is_active","is_manager","favorits","contacts","blacklist"]
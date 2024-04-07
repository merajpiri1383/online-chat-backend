# rest framework tools
from rest_framework import serializers
# get User model
from django.contrib.auth import get_user_model
# regex for password
import re

password_regex = re.compile(r"(?=.*[0-9])(?=.*[a-z]){8,16}")
# serializers  for registerations
class PhoneSerializer(serializers.ModelSerializer) :
    class Meta :
        model = get_user_model()
        fields = ["phone"]
    def validate(self,validated_data):
        phone = validated_data.get("phone")
        if len(phone) != 11 :
            raise serializers.ValidationError("phone number must be 11 character .")
        if not phone.isdigit() :
            raise serializers.ValidationError("phone number must be integer .")
        return validated_data

class PasswordSerializer(serializers.Serializer) :
    password = serializers.SlugField(required=True)
    confirm_password = serializers.SlugField(required=True)
    class Meta :
        model = get_user_model()
        fields = ["phone","password","confirm_password"]
    def validate(self,validated_data):
        if validated_data.get("password") != validated_data.get("confirm_password") :
            raise serializers.ValidationError("password and confrim arnt match .")
        if not password_regex.findall(validated_data.get("password")) :
            raise serializers.ValidationError("password must contains numbers and characters at least 8 ")
        return validated_data
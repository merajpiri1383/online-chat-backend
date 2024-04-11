# rest framework tools
from rest_framework import serializers
# get User model
from django.contrib.auth import get_user_model
# regex for password
import re
password_regex = re.compile(r"(?=.*[0-9])(?=.*[a-z]){8,16}")


class RegisterSerialzier(serializers.ModelSerializer) :
    password = serializers.SlugField(required=True)
    confirm_password = serializers.SlugField(required=True,write_only=True)
    class Meta :
        model = get_user_model()
        fields = ["id","phone","password","confirm_password"]

    def create(self,validated_data):
        user = get_user_model().objects.create(phone = validated_data["phone"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    # validation
    def validate(self,validated_data):
        # phone field
        if len(validated_data.get("phone")) != 11 :
            raise serializers.ValidationError("phone number must be 11 character .")

        if not validated_data.get("phone").isdigit() :
            raise serializers.ValidationError("phone number must be integer .")

        # password fields
        if validated_data.get("password") != validated_data.get("confirm_password") :
            raise serializers.ValidationError("password and confrim arnt match .")

        if not password_regex.findall(validated_data.get("password")) :
            raise serializers.ValidationError("password must contains numbers and characters at least 8 ")
        return validated_data

# reset password

class ResetPasswordSerializer(serializers.ModelSerializer) :
    confirm_password = serializers.SlugField(required=True, write_only=True)
    class Meta :
        model = get_user_model()
        fields = ["password","confirm_password"]
    def update(self,instance,validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance
    def validate(self, attrs):
        if not password_regex.findall(attrs.get("password")) :
            raise serializers.ValidationError("password must contains numbers and characters at least 8 ")
        return attrs
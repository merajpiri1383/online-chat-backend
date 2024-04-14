from rest_framework import serializers
from profuser.models import Profile

class ProfileSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Profile
        fields =["username","image","email"]
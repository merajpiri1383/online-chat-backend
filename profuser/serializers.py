from rest_framework import serializers
from profuser.models import Profile

class ProfileSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Profile
        fields =["id","username","image","email"]
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["phone"] = instance.user.phone
        return context
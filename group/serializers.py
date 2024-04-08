from difflib import context_diff

from rest_framework import serializers
from group.models import Group,MessageGroup
from user.serializer import UserSerializer
from django.contrib.auth import get_user_model

class MessageGroupSerializer(serializers.ModelSerializer) :
    class Meta :
        model = MessageGroup
        fields = ["group","create_by","created","updated"]

class GroupSerializer(serializers.ModelSerializer) :
    create_by = UserSerializer(read_only=True)
    messages = MessageGroupSerializer(many=True,read_only=True)
    class Meta :
        model = Group
        fields = ["id","name","create_by","messages"]
        read_only_fields = ["create_by","messages"]

    def create(self,validated_data):
        instance = Group.objects.create(
            create_by=self.context.get("request").user,
            **validated_data
        )
        return instance
    def to_representation(self,instance):
        context = super().to_representation(instance)
        context["create_time"] = instance.created.strftime("%H:%M:%S")
        context["create_date"] = instance.created.strftime("%Y-%m-%d")
        context["users"] = UserSerializer(instance.users,many=True).data
        return context
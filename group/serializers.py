from difflib import context_diff

from rest_framework import serializers
from group.models import Group,MessageGroup
from user.serializer import UserSerializer
from django.contrib.auth import get_user_model

class MessageGroupSerializer(serializers.ModelSerializer) :
    create_by = UserSerializer(read_only=True)
    class Meta :
        model = MessageGroup
        fields = ["id","group","create_by","text","file"]

    def to_representation(self,instance):
        context = super().to_representation(instance)
        context["create_time"] = instance.created.strftime("%H:%M:%S")
        context["create_date"] = instance.created.strftime("%Y-%m-%d")
        context["update_time"] = instance.updated.strftime("%H:%M:%S")
        context["update_date"] = instance.updated.strftime("%Y-%m-%d")
        return context

    def create(self,validated_data):
        message = MessageGroup.objects.create(
            create_by=self.context.get("request").user,
            **validated_data
        )
        return message
    def update(self,instance,validated_data):
        instance.text = validated_data.get("text")
        instance.file = validated_data.get("file")
        instance.save()
        return instance
    def validate(self,validated_data):
        user = self.context.get("request").user
        if not validated_data.get("text") and not validated_data.get("file") :
            raise serializers.ValidationError("وارد کردن متن یا فایل ضروری می باشد")
        if validated_data.get("group") :
            if not user in validated_data.get("group").users.all() and user != validated_data.get("group").create_by:
                raise serializers.ValidationError("شما در این گروه نمی باشد")
        return validated_data

class GroupSerializer(serializers.ModelSerializer) :
    create_by = UserSerializer(read_only=True)
    messages = MessageGroupSerializer(many=True,read_only=True)
    class Meta :
        model = Group
        fields = ["id","name","image","create_by","messages"]
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
        # un read messages
        un_read_messages = []
        for message in instance.messages.all() :
            if not self.context.get("request").user in message.readers() :
                un_read_messages.append(message)
        context["un_read_messages"] = MessageGroupSerializer(un_read_messages,many=True).data
        return context
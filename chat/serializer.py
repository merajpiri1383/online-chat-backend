from rest_framework import serializers
from chat.models import Chat , MessageChat
from user.serializer import UserSerializer
from django.contrib.auth import get_user_model

class MessageSerializer(serializers.ModelSerializer) :
    create_by = UserSerializer(read_only=True)
    def create(self,validated_data):
        user = self.context.get("request").user
        chat = Chat.objects.get(id=self.context["view"].kwargs.get("pk"))
        return MessageChat.objects.create(create_by=user,chat=chat,**validated_data)
    class Meta :
        model = MessageChat
        fields = ["id","create_by","chat","file","text"]
        required_fields = ["chat"]
    def validate(self,validated_date):
        if not validated_date.get("text") and not validated_date.get("file") :
            raise serializers.ValidationError("file or text is required .")
        return validated_date
    def to_representation(self,instance):
        context = super().to_representation(instance)
        context["create_time"] = instance.created.strftime("%H:%M:%S")
        context["create_date"] = instance.created.strftime("%Y-%m-%d")
        context["update_time"] = instance.updated.strftime("%H:%M:%S")
        context["update_date"] = instance.updated.strftime("%Y-%m-%d")
        return context

class ChatSerializer(serializers.ModelSerializer) :
    messages = MessageSerializer(many=True,read_only=True)

    # if this user has a chat with another user create method just get that chat and give you
    def create(self,validated_data):
        chat = self.context["request"].user.chats.filter(with_who=validated_data["with_who"]).first()
        if not chat :
            chat = Chat.objects.create(
                create_by = self.context["request"].user,
                with_who = validated_data["with_who"]
            )
        return chat
    class Meta :
        model = Chat
        fields = ["id","create_by","with_who","messages"]
        read_only_fields = ["create_by"]
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["create_by"] = UserSerializer(instance.create_by).data
        context["with_who"] = UserSerializer(instance.with_who).data
        # context["messages"] = MessageSerializer(instance.messages,many=True).data
        return context

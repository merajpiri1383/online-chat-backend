from rest_framework import serializers
from chat.models import Chat , MessageChat
from user.serializer import UserSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q

class MessageSerializer(serializers.ModelSerializer) :
    create_by = UserSerializer(read_only=True)
    class Meta :
        model = MessageChat
        fields = ["id","create_by","chat","file","text"]
        required_fields = ["chat"]
    def validate(self,attr):
        if not attr.get("text") and not attr.get("file") :
            raise serializers.ValidationError("file or text is required .")
        # check user is blocked or not
        attr["chat"] = Chat.objects.get(id=self.context["view"].kwargs.get("pk"))
        attr["create_by"] = self.context.get("request").user
        chat = attr.get("chat")
        if chat.create_by in chat.with_who.blacklist.all() or chat.with_who in chat.create_by.blacklist.all() :
            raise serializers.ValidationError("شما توسط این کاربر مسدود شده اید")
        return attr
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
    # with_who = serializers.PrimaryKeyRelatedField(
    #     required=True,
    #     queryset=get_user_model().objects.all()
    # )


    class Meta :
        model = Chat
        fields = ["id","create_by","with_who","messages"]
        read_only_fields = ["create_by"]

    def validate(self,attr):
        # check with_who is passed ?
        print(attr)
        if attr.get("with_who") in self.context.get("request").user.blacklist.all() :
            raise serializers.ValidationError("شما توسط این کاربر مسدود شده اید")
        return attr

    def create(self,validated_data):
        user = self.context.get("request").user
        instance_owner = user.chats.all().filter(with_who=validated_data.get("with_who"))
        instance_with_who = user.chats_with.all().filter(create_by=validated_data.get("with_who"))
        chat = instance_with_who.union(instance_owner).first()
        if not chat :
            chat = Chat.objects.create(
                create_by= user ,
                with_who= validated_data.get("with_who")
            )
        return chat

    def to_representation(self, instance):
        context = super().to_representation(instance)
        # context["messages"] = MessageSerializer(instance.messages,many=True).data
        context["create_by"] = UserSerializer(instance.create_by,context={"request":self.context["request"]}).data
        context["with_who"] = UserSerializer(instance.with_who,context={"request":self.context["request"]}).data
        return context

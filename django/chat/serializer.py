from rest_framework import serializers
from chat.models import Chat , Message
from user.serializer import UserSerializer


class MessageSerializer(serializers.ModelSerializer) :
    create_by = UserSerializer(read_only=True)
    class Meta :
        model = Message
        fields = ["id","create_by","chat","text","created","updated"]

class ChatSerializer(serializers.ModelSerializer) :
    create_by = UserSerializer(read_only =True)
    admins = UserSerializer(many=True)
    users = UserSerializer(many=True)
    messages = MessageSerializer(many=True)
    class Meta :
        model = Chat
        fields = ["id","create_by","admins","users","is_group","messages","group_image"]

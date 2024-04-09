# tools for rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (RetrieveDestroyAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
## permissions
from rest_framework.permissions import IsAuthenticated
from chat.permissions import IsInChat,IsInMessageOrNot
# classes created for chat
from chat.models import Chat , MessageChat
# serializer created for chat
from chat.serializer import MessageSerializer,ChatSerializer

# list all chats and create new one also get chat with post method
class ChatCreateAndListAPIView(ListCreateAPIView) :
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    def get_queryset(self):
        return self.request.user.chats_with.all().union(self.request.user.chats.all())
# get chat and destroy
class ChatAPIView(RetrieveDestroyAPIView) :
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated,IsInChat]

# create new message
class CreateMessageAPIView(CreateAPIView) :
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Chat.objects.all()

# get update and destroy a message
class MessageAPIView(RetrieveUpdateDestroyAPIView) :
    permission_classes = [IsInMessageOrNot]
    serializer_class = MessageSerializer
    queryset = MessageChat.objects.all()
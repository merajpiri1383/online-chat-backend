# tools for rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (RetrieveDestroyAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from rest_framework import status
## permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
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
        return self.request.user.chats.all().union(self.request.user.chats_with.all())


# get chat and destroy

class ChatAPIView(RetrieveDestroyAPIView) :
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated,IsInChat]

# getting chat messages and read them
class ReadMessageAPIView(APIView) :
    permission_classes = [IsAuthenticated, IsInChat]
    def get(self,request,pk):
        # getting chat
        try :
            chat = Chat.objects.get(id=pk)
            self.check_object_permissions(request,chat)
        except :
            return Response(data={"detail":"chat with this id does not exist"},status=status.HTTP_400_BAD_REQUEST)
        for message in chat.messages.all() :
            if not request.user in message.readers() :
                message.users_read.add(request.user)
        return Response(data=ChatSerializer(chat,context={"request":request}).data)


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
    
    
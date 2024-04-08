# tools for rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
## permissions
from rest_framework.permissions import IsAuthenticated
from chat.permissions import IsOwnerOrNot
# classes created for chat
from chat.models import Chat , MessageChat
# serializer created for chat
from chat.serializer import MessageSerializer,ChatSerializer

# list all chats and create new one also get chat with post method
class ChatCreateAndListAPIView(APIView) :

    permission_classes = [IsAuthenticated]

    # list all chats that current user have
    def get(self,request):
        chats = request.user.chats.all()
        return Response(data=ChatSerializer(chats,many=True).data)

    # if current user has a chat with another user , post method just give that
    # if not exist that chat create one
    def post(self,request):
        # send request in context to avoid query again to database for getting user
        serializer = ChatSerializer(data=request.data,context={"request":request})
        if serializer.is_valid() :
            serializer.save()
            return Response(
                data=serializer.data ,
                status = status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors ,
            status = status.HTTP_400_BAD_REQUEST
        )

# get chat and destroy
class ChatAPIView(RetrieveDestroyAPIView) :
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrNot]

# create new message
class CreateMessageAPIView(CreateAPIView) :
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Chat.objects.all()

# get update and destroy a message
class MessageAPIView(RetrieveUpdateDestroyAPIView) :
    permission_classes = [IsOwnerOrNot]
    serializer_class = MessageSerializer
    queryset = MessageChat.objects.all()
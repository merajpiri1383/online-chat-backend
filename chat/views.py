# tools for rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
## permissions
from rest_framework.permissions import IsAuthenticated
# classes created for chat
from chat.models import Chat , Message
# serializer created for chat
from chat.serializer import MessageSerializer,ChatSerializer

# list all chats and create new one
class ChatCreateAndListAPIView(APIView) :

    permission_classes = [IsAuthenticated]

    def get(self,request):
        chats = request.user.chats.all()
        return Response(data=ChatSerializer(chats,many=True).data)

    def post(self,request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(
                data=serializer.data ,
                status = status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.error ,
            status = status.HTTP_400_BAD_REQUEST
        )
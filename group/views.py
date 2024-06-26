# rest framework tools
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
# models
from group.models import Group,MessageGroup
from django.contrib.auth import get_user_model
# serializers
from group.serializers import MessageGroupSerializer,GroupSerializer
# permissions
from group.permissions import IsOwnerGroupOrNot,IsOwnerMessageOrReadOnly,IsOwnerGroupOrInGroupReadOnly
from rest_framework.permissions import IsAuthenticated

# get all groups for a user or create one
class GroupListCreateAPIView(ListCreateAPIView) :
    serializer_class = GroupSerializer
    def get_queryset(self):
        return self.request.user.group_chats.all().union(self.request.user.group_set.all())
    permission_classes = [IsAuthenticated]


class UserGroupAPIView(APIView) :

    permission_classes = [IsAuthenticated,IsOwnerGroupOrInGroupReadOnly]

    def get_user(self):
        if not self.request.data.get("phone") :
            return Response(data={"detail":"شماره ضروری می باشد"})
        try :
            self.user = get_user_model().objects.get(phone=self.request.data["phone"])
        except :
            return Response(data={"detail":"کاربری با این شماره وجود ندارد"},status=status.HTTP_400_BAD_REQUEST)
    def get_group(self):
        if not self.request.data.get("group") :
            return Response(data={"detail":"group is required ."},status=status.HTTP_400_BAD_REQUEST)
        try :
            self.group = Group.objects.get(id=self.request.data.get("group"))
        except :
            return Response(data={"detail":"group not found ."},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        if self.get_group() :
            return self.get_group()
        if self.get_user() :
            return self.get_user()
        self.check_object_permissions(self.request, self.group)
        self.group.users.add(self.user)
        return Response(data=GroupSerializer(self.group,context={"request":request}).data)
    def delete(self,request):
        if self.get_group() :
            return self.get_group()
        if self.get_user() :
            return self.get_user()
        self.check_object_permissions(self.request, self.group)
        self.group.users.remove(self.user)
        return Response(data=GroupSerializer(self.group,context={"request":request}).data)

# get update and delete group
class GroupAPIView(RetrieveUpdateDestroyAPIView) :
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated,IsOwnerGroupOrInGroupReadOnly]

# sending message to the group
class CreateMessageGroupAPIView(CreateAPIView) :
    permission_classes = [IsAuthenticated]
    serializer_class = MessageGroupSerializer

# get retreive update destroy message
class MessageGroupAPIView(RetrieveUpdateDestroyAPIView) :
    permission_classes = [IsAuthenticated,IsOwnerMessageOrReadOnly]
    serializer_class = MessageGroupSerializer
    queryset = MessageGroup.objects.all()

# read messages in group
class ReadMessagesGroupAPIView(APIView) :

    permission_classes = [IsAuthenticated,IsOwnerGroupOrInGroupReadOnly]
    def get(self,request,pk):

        # getting the group
        try :
            group = Group.objects.get(id=pk)
        except :
            return Response(data={"detail":"group with this id does not exist"},status=status.HTTP_400_BAD_REQUEST)
        for message in group.messages.all() :
            if request.user not in message.readers() :
                message.users_read.add(request.user)
        return Response(data=GroupSerializer(group,context={"request":request}).data)
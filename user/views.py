from django.contrib.auth import get_user_model
# rest framework tools
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# serializers
from user.serializer import UserSerializer,MoreInfoUserSerializer
# permissions
from rest_framework.permissions import IsAuthenticated

class ListUserAPIView(ListAPIView) :
    queryset = get_user_model().objects.filter(is_superuser=False)
    serializer_class = UserSerializer


class FavoritAPIView(APIView) :
    permission_classes = [IsAuthenticated]

    def get_user(self,request):
        # check phone is passd ?
        if not request.data.get("phone"):
            return Response("phone is required .", status=status.HTTP_400_BAD_REQUEST)
        # check phone is valid
        try:
            self.user = get_user_model().objects.get(phone=request.data.get("phone"))
        except:
            return Response(data={"detail": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self,request):
        serializer = UserSerializer(request.user.favorits.all(),many=True)
        return Response(data=serializer.data)
    def post(self,request):
        if self.get_user(request) :
            return self.get_user(request)
        request.user.favorits.add(self.user)
        return Response(data=MoreInfoUserSerializer(request.user).data)
    def delete(self,request):
        if self.get_user(request) :
            return self.get_user(request)
        request.user.favorits.remove(self.user)
        return Response(data=MoreInfoUserSerializer(request.user).data)

class ContactAPIView(APIView) :
    permission_classes = [IsAuthenticated]

    def get_user(self,request):
        # check phone is passd ?
        if not request.data.get("phone"):
            return Response({"detail":"phone is required ."}, status=status.HTTP_400_BAD_REQUEST)
        # check phone is valid
        try:
            self.user = get_user_model().objects.get(phone=request.data.get("phone"))
        except:
            return Response(data={"detail": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self,request):
        serializer = UserSerializer(request.user.contacts.all(),many=True)
        return Response(data=serializer.data)
    def post(self,request):
        if self.get_user(request) :
            return self.get_user(request)
        request.user.contacts.add(self.user)
        return Response(data=MoreInfoUserSerializer(request.user).data)
    def delete(self,request):
        if self.get_user(request) :
            return self.get_user(request)
        request.user.contacts.remove(self.user)
        return Response(data=MoreInfoUserSerializer(request.user).data)
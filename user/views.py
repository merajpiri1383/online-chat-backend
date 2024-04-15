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


# get user func
def get_user(request):
    # check phone is passd ?
    if not request.data.get("phone"):
        return Response({"detail": "شماره ضروری می باشد"}, status=status.HTTP_400_BAD_REQUEST)
    # check phone is valid
    try:
        return get_user_model().objects.get(phone=request.data.get("phone"))
    except:
        return Response(data={"detail": "کاربری با این شماره وجود ندارد"}, status=status.HTTP_404_NOT_FOUND)
class ListUserAPIView(ListAPIView) :
    queryset = get_user_model().objects.filter(is_superuser=False)
    serializer_class = UserSerializer


class FavoritAPIView(APIView) :
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user.favorits.all(),many=True)
        return Response(data=serializer.data)

    def post(self,request):
        result = get_user(request)
        if not isinstance(result, get_user_model()):
            return result
        request.user.favorits.add(result)
        return Response(data=MoreInfoUserSerializer(request.user).data)

    def delete(self,request):
        result = get_user(request)
        if not isinstance(result, get_user_model()):
            return result
        request.user.favorits.remove(result)
        return Response(data=MoreInfoUserSerializer(request.user).data)

class ContactAPIView(APIView) :
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = MoreInfoUserSerializer(request.user)
        return Response(data=serializer.data)
    def post(self,request):
        result = get_user(request)
        if not isinstance(result, get_user_model()):
            return result
        request.user.contacts.add(result)
        return Response(data=MoreInfoUserSerializer(request.user).data)
    def delete(self,request):
        result = get_user(request)
        if not isinstance(result, get_user_model()):
            return result
        request.user.contacts.remove(result)
        return Response(data=MoreInfoUserSerializer(request.user).data)

# black list

class BlacklistAPIView(APIView) :

    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user.blacklist.all(),many=True)
        return Response(data=serializer.data)

    def post(self,request):
        result = get_user(request)
        if not isinstance(result, get_user_model()):
            return result
        request.user.blacklist.add(result)
        return Response(data=MoreInfoUserSerializer(request.user).data)

    def delete(self,request):
        result = get_user(request)
        if not isinstance(result, get_user_model()):
            return result
        request.user.blacklist.remove(result)
        return Response(data=MoreInfoUserSerializer(request.user).data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from profuser.models import Profile
from profuser.serializers import ProfileSerializer
from user.serializer import MoreInfoUserSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from profuser.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model



class ProfileAPIView(APIView) :
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    def get(self,request):
        serializer = MoreInfoUserSerializer(instance=request.user)
        return Response(data=serializer.data)
    def put(self,request):
        serializer = ProfileSerializer(data=request.data,instance=request.user.profile)
        if serializer.is_valid() :
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailAPIView(RetrieveAPIView) :
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
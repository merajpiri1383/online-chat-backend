from django.contrib.auth import get_user_model
# rest framework tools
from rest_framework.generics import ListAPIView
# serializers
from user.serializer import UserSerializer

class ListUserAPIView(ListAPIView) :
    queryset = get_user_model().objects.filter(is_superuser=False)
    serializer_class = UserSerializer
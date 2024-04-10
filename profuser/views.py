from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView
from profuser.models import Profile
from profuser.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from profuser.permissions import IsOwnerOrReadOnly

class ProfileList(ListAPIView) :
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileAPIView(RetrieveUpdateAPIView) :
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
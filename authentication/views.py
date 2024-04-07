# rest framework tools
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# user
from django.contrib.auth import get_user_model
from user.serializer import UserSerializer
# documenting with swagger
from drf_spectacular.utils import extend_schema, OpenApiParameter
# jwt tokem
from rest_framework_simplejwt.tokens import RefreshToken

# login
class LoginAPIView(APIView) :
    # documenting
    @extend_schema(
        parameters=[
            OpenApiParameter(name="phone",required=True),
            OpenApiParameter(name="password",required=True)
        ]
    )

    def post(self,request):
        # check phone and password is exist
        if not request.data.get("phone") :
            return Response(data={"detail":"phone is required ."},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("password") :
            return Response(data={"detail":"password is required ."},status=status.HTTP_400_BAD_REQUEST)

        # check user exist
        try :
            user = get_user_model().objects.get(phone=request.data.get("phone"))
        except :
            return Response(data={"detail":"user doesnt exist ."},status=status.HTTP_400_BAD_REQUEST)
        if user.check_password(request.data.get("password")) :
            token = RefreshToken.for_user(user)
            return Response(data={
                "user": UserSerializer(user).data,
                "access_token": str(token.access_token),
                "refresh_token" : str(token),
            })
        else :
            return Response(data={"detail":"password or phone is incorrect ."},
                            status=status.HTTP_400_BAD_REQUEST)
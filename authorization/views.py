# rest framework tools for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# get User model
from django.contrib.auth import get_user_model
# jwt authentication
# serializers for registerations
from authorization.serializers import PhoneSerializer,PasswordSerializer
# documenting
from drf_spectacular.utils import extend_schema,OpenApiParameter
# tasks
from authorization.tasks import delete_user,send_sms
from celery import chain
# jwt tokens
from user.serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# permissions
from authorization.permissions import IsOwnerOrNot
# handling registeration for user
class RegisterPhoneAPIView(APIView) :
    serializer_class = PhoneSerializer
    @extend_schema(
        parameters=[
            OpenApiParameter(name="phone", description="phone number for registeration", required=True)
        ]
    )
    def post(self,request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid() :
            user = serializer.save()
            # send activation code using celery and rabbitmq
            # check that if user not activate after 120s user delete
            tasks = chain(send_sms.s(user.phone,user.otp),delete_user.s())()
            return Response(data={"detail":f"activation code is sent "})
        return Response(
            data=serializer.errors ,
            status = status.HTTP_400_BAD_REQUEST
        )


# verify
class VerifyPhoneAPIView(APIView) :
    # sagger
    @extend_schema(
        parameters=[
            OpenApiParameter(name="phone",description="phone number of user",required=True),
            OpenApiParameter(name="otp",description="otp code ",required=True)
        ]
    )


    def post(self,request):
        if not request.data.get("phone") :
            return Response(data={"detail":"phone number is required"},status=status.HTTP_400_BAD_REQUEST)
        try :
            user = get_user_model().objects.get(phone=request.data.get("phone"))
        except :
            return Response(data={"detail":"user with this phone doesnt exist "},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("otp") == user.otp :
            user.is_active = True
            user.save()
            refresh_token = RefreshToken.for_user(user)

            return Response(data={
                "user" : UserSerializer(user).data,
                "access_token" : str(refresh_token.access_token),
                "refresh_token" : str(refresh_token)
            })
        else :
            return Response(data={"detail":"invalid otp"},status=status.HTTP_400_BAD_REQUEST)

# set passsword
class SetPasswordAPIView(APIView) :
    serializer_class = PasswordSerializer
    permission_classes = [IsOwnerOrNot]
    @extend_schema(
        parameters=[
            OpenApiParameter(name="phone",description="phone number",required=True),
            OpenApiParameter(name="password",description="must be between 8,16 character",required=True),
            OpenApiParameter(name="confirm_password",required=True)
        ]
    )

    def post(self,request):
        # get user
        if not request.data.get("phone") :
            return Response(data={"detail":"phone number is required"},status=status.HTTP_400_BAD_REQUEST)
        try :
            user = get_user_model().objects.get(phone=request.data.get("phone"))
        except :
            return Response(
                data={"detail":"user with this phone doenst exist ."},
                status = status.HTTP_400_BAD_REQUEST
            )
        self.check_object_permissions(request,user)
        serializer = PasswordSerializer(data=request.data,instance=user)
        if serializer.is_valid() :
            user.set_password(request.data.get("password"))
            user.save()
            return Response(data={"detail":"ok"})
        else :
            return Response (
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
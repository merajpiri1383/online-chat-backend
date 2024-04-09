# rest framework tools for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# get User model
from django.contrib.auth import get_user_model
# jwt authentication
# serializers for registerations
from account.serializers import RegisterSerialzier,ResetPassword
# documenting
from drf_spectacular.utils import extend_schema,OpenApiParameter
# tasks
from account.tasks import delete_user,send_sms,forget_password
from celery import chain
# jwt tokens
from user.serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# handling registeration for user
class RegisterAPIView(APIView) :
    serializer_class = RegisterSerialzier
    @extend_schema(
        parameters=[
            OpenApiParameter(name="phone", description="phone number for registeration", required=True)
        ]
    )
    def post(self,request):
        serializer = RegisterSerialzier(data=request.data)
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
class VerifyAPIView(APIView) :
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
            user = get_user_model().objects.get(phone=request.data.get("phone"),is_active=True)
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

# forget password and send otp code for reseting
class ForegetPasswordAPIView(APIView) :
    # documenting
    @extend_schema(
        parameters=[
            OpenApiParameter(name="phone",required=True)
        ]
    )
    def post(self,request):
        # check phone is passed
        if not request.data.get("phone") :
            return Response(data={"detail":"phone is required ."} , status=status.HTTP_400_BAD_REQUEST)
        # send otp to user
        forget_password.apply_async(args=[request.data.get("phone")])
        return Response(data={"detail":"code is sent ."})

class ResetPasswordAPIView(APIView) :
    def put(self,request):
        try :
            user = get_user_model().objects.get(phone=request.data.get("phone"))
        except :
            return Response(data={"detail":"user with this phone does not exist ."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ResetPassword(data=request.data,instance=user)
        if serializer.is_valid() :
            serializer.save()
            return Response(data=UserSerializer(user).data)
        else :
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
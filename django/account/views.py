# rest framework tools for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# get User model
from django.contrib.auth import get_user_model
# jwt authentication
from rest_framework_simplejwt.models import Token
# serializers for registerations
from account.serializers import PhoneSerializer



# handling registeration for user

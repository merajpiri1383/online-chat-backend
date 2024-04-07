from rest_framework import serializers
# get User model
from django.contrib.auth import get_user_model

# serializers  for registerations
class PhoneSerializer(serializers.ModelSerializer) :
    class Meta :
        model = get_user_model()
        fields = ["phone"]
    def clean(self,data):
        print(data)
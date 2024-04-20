from django.urls import path
from chat import views

urlpatterns = [
    # messages
    path("<pk>/messages/",views.ReadMessageAPIView.as_view()),
    path("",views.ChatCreateAndListAPIView.as_view()),
    # you can get all message of a chat by getting messages
    path("<pk>/",views.ChatAPIView.as_view()),
    # create a new message
    path("<pk>/message/create/",views.CreateMessageAPIView.as_view()),
    # get update and destroy a message
    path("message/<pk>/",views.MessageAPIView.as_view()),
]
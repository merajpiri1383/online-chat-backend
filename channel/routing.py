from channel import consumer
from django.urls import path 

urlpatterns_websocket = [
    path("ws/user/",consumer.MessageChatConsumer.as_asgi()),
]
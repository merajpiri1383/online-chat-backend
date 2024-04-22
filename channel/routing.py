from channel import consumer
from django.urls import path 

urlpatterns_websocket = [
    path("ws/chat/<chat_id>/",consumer.MessageChatConsumer.as_asgi()),
]
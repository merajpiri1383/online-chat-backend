from django.db import models
from django.contrib.auth import get_user_model
# jalali date
from django_jalali.db.models import jDateTimeField
class Chat(models.Model) :
    create_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="chats")
    with_who = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="chats_with")
    created = jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat  {self.create_by} "
# class ChatGroup(models.Model) :
#     create_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="owner_groups")
#     user = models.ManyToManyField(get_user_model(),related_name="chat_groups")
#     admins = models.ManyToManyField(get_user_model())
#     created = jDateTimeField(auto_now_add=True)

class Message(models.Model) :
    create_by = models.ForeignKey(get_user_model(),related_name="messages",on_delete=models.CASCADE)
    created = jDateTimeField(auto_now_add=True)
    updated = jDateTimeField(auto_now=True)
    class Meta :
        abstract = True
class MessageChat(Message) :
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", null=True)
    text = models.TextField(null=True)
    file = models.FileField(upload_to="chat/messages/files",null=True)
    # if message is response of another message
    sub_message = models.ForeignKey(
        "MessageChat",
        on_delete=models.CASCADE,
        related_name="sub_messages",
        null=True,
        blank=True)
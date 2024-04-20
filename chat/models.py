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


class Message(models.Model) :
    create_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to="chat/messages/files", null=True,blank=True)
    created = jDateTimeField(auto_now_add=True)
    updated = jDateTimeField(auto_now=True)

    def readers(self) :
        return self.users_read.all()
    class Meta :
        abstract = True

class MessageChat(Message) :
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", null=True)
    users_read = models.ManyToManyField(get_user_model(),related_name="users_read",blank=True)
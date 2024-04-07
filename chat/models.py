from django.db import models
from django.contrib.auth import get_user_model
# jalali date
from django_jalali.db.models import jDateTimeField
class Chat(models.Model) :
    create_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="chats")
    admins = models.ManyToManyField(get_user_model())
    users = models.ManyToManyField(get_user_model(), related_name="group_chats")
    created = jDateTimeField(auto_now_add=True)
    is_group = models.BooleanField(default=False)
    group_image = models.ImageField(upload_to="group_chats",null=True,blank=True)

    def __str__(self):
        return f"Chat  {self.create_by} "

class Message(models.Model) :
    user = models.ForeignKey(get_user_model(),related_name="messages",on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name="messages")
    text = models.TextField()
    created = jDateTimeField(auto_now_add=True)
    updated = jDateTimeField(auto_now=True)
    # if message is response of another message
    sub_message = models.ForeignKey(
        "Message",
        on_delete=models.CASCADE,
        related_name="sub_messages",
        null=True,
        blank=True)
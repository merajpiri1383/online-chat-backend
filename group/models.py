from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db.models import jDateTimeField
from chat.models import Message

class Group(models.Model) :
    name = models.CharField(max_length=128,unique=True)
    create_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="group_chats")
    created = jDateTimeField(auto_now_add=True)
    users = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.name

class MessageGroup(Message) :
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="messages")
    create_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    created = jDateTimeField(auto_now_add=True)
    updated = jDateTimeField(auto_now=True)
    sub_message = models.ForeignKey(
        "MessageGroup",
        on_delete=models.SET_NULL,
        null=True
    )
from django.db import models
from django.contrib.auth import get_user_model
from django.core.cache import cache

class Profile(models.Model) :
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name="profile")
    username = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    image = models.ImageField(upload_to="user/images", null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.username}"
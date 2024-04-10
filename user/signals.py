from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from profuser.models import Profile

@receiver(signal=post_save,sender=get_user_model())
def create_profile(sender,instance,created,**kwargs) :
    if created :
        Profile.objects.create(user=instance)
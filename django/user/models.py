from django.db import models
# user manager for custom user model
from user.manager import UserManager
# base model for creating custom user model and essential permissions
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# jalali date
from django_jalali.db.models import jDateTimeField
# create random for otp
from random import randint
# custom user model
class User(AbstractBaseUser,PermissionsMixin):

    # use phone instead of username field
    phone = models.SlugField(
        unique=True,
        max_length=11
    )

    # fields for detemaine user permissions
    is_active = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # date user joined used django-jalali packages
    date_joined = jDateTimeField(auto_now_add=True)

    # otp code
    otp = models.SlugField(max_length=6,blank=True,null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    # manager
    objects = UserManager()

    def __str__(self):
        return str(self.phone)

    @property
    def is_staff(self):
        return self.is_manager

    # change otp code every time user saved
    def save(self,**kwargs):
        self.otp = randint(100000,999999)
        return super().save(**kwargs)
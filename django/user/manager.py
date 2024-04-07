from django.contrib.auth.models import BaseUserManager

# manager for Custom User Model

class UserManager(BaseUserManager) :

    # create user for user manager
    def create_user(self,phone,password,**kwargs):
        if not phone :
            raise  ValueError("phone number is required .")
        user = self.model(phone=phone,**kwargs)
        if password :
            user.set_password(password)
        return user.save()

    # create superuser called when createsuperuser
    def create_superuser(self,phone,password,**kwargs):
        kwargs.setdefault("is_active",True)
        kwargs.setdefault("is_manager",True)
        kwargs.setdefault("is_superuser",True)
        return self.create_user(phone=phone,password=password,**kwargs)
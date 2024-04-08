from rest_framework.permissions import BasePermission

class IsOwnerGroupOrNot(BasePermission) :
    def has_object_permission(self,request,view,object):
        if request.user.is_authenticated :
            return object in request.user.group_chats.all()
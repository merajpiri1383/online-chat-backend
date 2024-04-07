from rest_framework.permissions import BasePermission

class IsOwnerOrNot(BasePermission) :

    def has_object_permission(self,request,view,object):
        if request.user.is_authenticated :
            return object.phone == request.user.phone
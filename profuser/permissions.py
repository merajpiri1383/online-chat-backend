from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission) :
    def has_object_permission(self,request,view,object):
        if request.user.is_authenticated :
            if request.method in SAFE_METHODS :
                return True
            else :
                return request.user == object.user
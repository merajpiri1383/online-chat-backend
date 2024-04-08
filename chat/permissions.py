from rest_framework.permissions import BasePermission

class IsOwnerOrNot(BasePermission) :
    def has_object_permission(self,request,view,obj):
        if request.user.is_authenticated :
            return request.user == obj.create_by
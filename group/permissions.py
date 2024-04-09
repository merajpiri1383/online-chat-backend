from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsOwnerGroupOrNot(BasePermission) :
    def has_object_permission(self,request,view,object):
        if request.user.is_authenticated :
            return object in request.user.group_chats.all()

class IsOwnerGroupOrInGroupReadOnly(BasePermission) :
    def has_object_permission(self,request,view,object):
        if request.user.is_authenticated :
            user = request.user
            if request.method in SAFE_METHODS :
                return user in object.users.all() or user == object.create_by
            else :
                return object in request.user.group_chats.all()



class IsOwnerMessageOrReadOnly(BasePermission) :
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated :
            if request.method in SAFE_METHODS :
                return request.user in obj.group.users.all() or request.user == obj.create_by
            else :
                return obj.create_by == request.user
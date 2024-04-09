from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsInChat(BasePermission) :
    def has_object_permission(self,request,view,obj):
        if request.user.is_authenticated :
            return request.user == obj.create_by or request.user == obj.with_who

class IsInMessageOrNot(BasePermission) :
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated :
            if request.method in SAFE_METHODS :
                return request.user == obj.chat.create_by or request.user == obj.chat.with_who
            else :
                return request.user == obj.create_by
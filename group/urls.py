from django.urls import path
from group import views

urlpatterns = [
    path("",views.GroupListCreateAPIView.as_view()),
    # change users of group
    path("user/change/",views.UserGroupAPIView.as_view()),
]
from django.urls import path
from group import views

urlpatterns = [
    # get list of grous
    path("",views.GroupListCreateAPIView.as_view()),
    # get update and destroy group
    path("<pk>/",views.GroupAPIView.as_view()),
    # change users of group
    path("user/change/",views.UserGroupAPIView.as_view()),
    # send message in group
    path("message/create/",views.CreateMessageGroupAPIView.as_view()),
    # get , update , destroy message
    path("message/<pk>/",views.MessageGroupAPIView.as_view()),
]
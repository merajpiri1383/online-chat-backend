from django.urls import path
from user import views

urlpatterns = [
    path("list/",views.ListUserAPIView.as_view()),
]
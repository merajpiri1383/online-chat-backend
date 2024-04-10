from django.urls import path
from profuser import views

urlpatterns = [
    path("",views.ProfileList.as_view()),
    path("<pk>/",views.ProfileAPIView.as_view()),
]
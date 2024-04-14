from django.urls import path
from profuser import views

urlpatterns = [
    path("",views.ProfileAPIView.as_view()),
    path("<pk>/",views.ProfileDetailAPIView.as_view()),
]
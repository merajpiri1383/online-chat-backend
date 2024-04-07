from django.urls import path
from account import views

urlpatterns = [
    path("register/", views.RegisterAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("verify/", views.VerifyAPIView.as_view()),
    path("password/forget/",views.ForegetPasswordAPIView.as_view()),
    path("password/reset/",views.ResetPasswordAPIView.as_view()),
]
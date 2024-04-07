from django.urls import path
from authorization import views

urlpatterns = [
    # registeration
    path("register/",views.RegisterPhoneAPIView.as_view()),
    path("register/verify/",views.VerifyPhoneAPIView.as_view()),
    path("password/change/",views.SetPasswordAPIView.as_view()),
]
from django.urls import path
from user import views

urlpatterns = [
    path("list/",views.ListUserAPIView.as_view()),
    path("favorits/",views.FavoritAPIView.as_view()),
    path("contacts/",views.ContactAPIView.as_view()),
    path("blacklist/",views.BlacklistAPIView.as_view()),
]
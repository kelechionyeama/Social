from django.urls import path
from . import views

urlpatterns =[
    path("friendship-list", views.ListFriendsAPIView.as_view()),
    path("friendship-update", views.UpdateFriendship, name="update"),
    path("friendship-delete", views.DeleteFriendship, name="update")
]

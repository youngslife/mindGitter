from django.urls import path
from accounts.views import CurrentUserAPIView, ProfileImageAPIView, NotificationAPIView


urlpatterns = [
    path("current_user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("profile_img/", ProfileImageAPIView.as_view(), name="profile-img"),
    path("notifications/", NotificationAPIView.as_view(), name="notification"),
]
from django.urls import path
from accounts.views import CurrentUserAPIView, ProfileImageAPIView, UserNameAPIView


urlpatterns = [
    path("current_user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("profile_img/", ProfileImageAPIView.as_view(), name="profile-img"),
    path("user/<int:user_pk>/", UserNameAPIView.as_view(), name="user-detail")
]
from django.urls import path
from accounts.views import CurrentUserAPIView, ProfileImageAPIView, UserNameAPIView, NotificationAPIView, NoticeDetail


urlpatterns = [
    path("current_user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("profile_img/", ProfileImageAPIView.as_view(), name="profile-img"),
    path("user/<int:user_pk>/", UserNameAPIView.as_view(), name="user-detail"),
    path("notifications/", NotificationAPIView.as_view(), name="notification"),
    path("notifications/<int:notice_id>/", NoticeDetail.as_view(), name="notice-detail")
]
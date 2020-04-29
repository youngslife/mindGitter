from django.urls import path
<<<<<<< HEAD
from accounts.views import CurrentUserAPIView, ProfileImageAPIView, NotificationAPIView
=======
from accounts.views import CurrentUserAPIView, ProfileImageAPIView, UserNameAPIView
>>>>>>> 6b5ddcdb09ca1a82f07db745a46c892585b6f305


urlpatterns = [
    path("current_user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("profile_img/", ProfileImageAPIView.as_view(), name="profile-img"),
<<<<<<< HEAD
    path("notifications/", NotificationAPIView.as_view(), name="notification"),
=======
    path("user/<int:user_pk>/", UserNameAPIView.as_view(), name="user-detail")
>>>>>>> 6b5ddcdb09ca1a82f07db745a46c892585b6f305
]
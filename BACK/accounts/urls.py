from django.urls import path
from accounts.views import CurrentUserAPIView


urlpatterns = [
    path("current_user/", CurrentUserAPIView.as_view(), name="current-user")
]
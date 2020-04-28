from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.serializers import UserDisplaySerializer, ProfileImageSerializer, NotificationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import User, Notification


class CurrentUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)


class ProfileImageAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = ProfileImageSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):  # profile_img 넘겨줘야함
        user = request.user
        # profile_img = request.user.profile_img
        # profile_img.delete()
        serializer = ProfileImageSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # def delete(self, request):
    #     profile_img = request.user.profile_img
    #     profile_img.delete()
    #     return Response(status=204)


class NotificationAPIView(APIView):
    def get(self, request, format=None):
        user = request.user
        notifications = Notification.objects.filter(to=user)
        serializer = NotificationSerializer(notification, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def create_notification(request, inviter, to, notification_type):
    print(inviter, to, notification_type)
    
    notifications = Notification.objects.create(
        inviter = inviter,
        to = to,
        notification_type = notification_type
        # comment = comment
    )

    notifications.save()
    
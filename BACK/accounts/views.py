from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.serializers import UserDisplaySerializer, ProfileImageSerializer, NotificationSerializer, UserNameSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import User, Notification
from channels.models import Channel


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


class UserNameAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, user_pk):
        user = get_object_or_404(get_user_model(), pk=user_pk)
        user_serializer = UserNameSerializer(user)
        return Response(user_serializer.data)


class NotificationAPIView(APIView): 
    permission_classes = (IsAuthenticated,)

    def get(self, request): # 해당 user가 guest인 모든 notification
        user = get_object_or_404(User, id=request.user.id)
        notifications = Notification.objects.filter(guest=user.id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request): # Body(user, channel_id, notification_type)
        guest = get_object_or_404(User, username=request.data.get('username'))
        channel = get_object_or_404(Channel, id=request.data.get('channel_id'))
        inviter = get_object_or_404(User, id=request.user.id)
        data = {'inviter': inviter.id,
                'guest': guest.id,
                'notice_type': request.data.get('notice_type'),
                'channel': channel.id,
                'accept_or_not': "0",
                }
        print('##########', data)
        
        notifications = NotificationSerializer(data=data)
        if notifications.is_valid():
            notifications.save()
        # notifications = Notification.objects.create(
        #             inviter = inviter,
        #             to = to,
        #             notification_type = request.data.notification_type
        #             # comment = comment
        #         )
        
            return Response(notifications.data, status=status.HTTP_201_CREATED)  # 응답 굳이 이형태로 주지 않아도 될듯
        return Response(notifications.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticeDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, notice_id): # 1개
        notification = Notification.objects.filter(id=notice_id)
        serializer = NotificationSerializer(notification, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def put(self, request, notice_id):
        
        notification = Notification.objects.get(id=notice_id)
        # data = request.data.dict()
        data = request.data

        data.update({'inviter': notification.inviter.id,
                    'guest': notification.guest.id,
                    'channel': notification.channel.id,
                    'notice_type': notification.notice_type
                })
        # data.update({'guest': notification.guest.id})
        # data.update({'channel': notification.channel.id})
        # data.update({'notice_type': notification.notice_type})

        serializer = NotificationSerializer(instance=notification, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# def create_notification(request, inviter, to, notification_type):
#     print(inviter, to, notification_type)
    
#     notifications = Notification.objects.create(
#         inviter = inviter,
#         to = to,
#         notification_type = notification_type
#         # comment = comment
#     )

#     notifications.save()
    


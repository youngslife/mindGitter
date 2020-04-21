from django.shortcuts import render
from .models import Channel
from rest_framework import status
from rest_framework.decorators import api_view
from accounts.models import User
from accounts.serializers import UserDisplaySerializer
from .serializers import UserChannelSerializer, ChannelSerializer
import jwt
from django.http import JsonResponse
from back.settings import SECRET_KEY
from datetime import datetime

# Create your views here.

# 채널 목록
@api_view(['GET', 'POST'])
def board(request):
    if request.method == 'GET':  # list of diary books
        user = User.objects.get(username=request.user)
        serializers = UserChannelSerializer(user)
        return JsonResponse(serializers.data)

    elif request.method == 'POST':  # create a diary book
        user = User.objects.get(username=request.user)
        Channel.objects.create(
            title=request.data.get('title'),
            cover_image=request.data.get('cover_image'),
            description=request.data.get('description'),
            create_user=user
        )
        channel = Channel.objects.last()
        user.channels.add(channel)

        serializers = ChannelSerializer(channel)
        return JsonResponse(serializers.data)
        # print(serializers)

        # if serializers.is_valid():
        #     channel = Channel.objects.last()
        #     user.channels.add(channel)
        #     serializers.save()
        #     return JsonResponse({'message': 'success to save'}, status=201)
        # else:
        #     return JsonResponse({'message': 'fail to save'}, status=400)


# 채널 한 개
@api_view(['GET', 'PUT', 'DELETE'])
def board_title(request, id):
    if request.method == 'GET':  # diary book detail
        channel = Channel.objects.get(id=id)
        serializer = ChannelSerializer(channel)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':  # update a diary book
        channel = Channel.objects.get(id=id)
        serializer = ChannelSerializer(channel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'success to update'}, status=201)
        else:
            return JsonResponse({'message': 'fail to update'}, status=400)

    elif request.method == 'DELETE':  # delete a diary book
        channel = Channel.objects.get(id=id)
        channel.delete()
        return JsonResponse({'message': 'success to delete'}, status=200)


# 채널 입장 및 탈퇴
@api_view(['POST', 'DELETE'])
def board_join(request, id):
    if request.method == 'POST':  # join a channel
        user = User.objects.get(username=request.user)
        channel = Channel.objects.get(id=id)
        user.channels.add(channel)
        return JsonResponse({'message': 'success to join'}, status=201)

    elif request.method == 'DELETE':  # leave from a channel
        user = request.user
        channel = Channel.objects.get(id=id)
        if channel.user_set.filter(id=user.id).exists():
            channel.user_set.remove(user)
            return JsonResponse({'message': 'success to leave'}, status=200)
        else:
            return JsonResponse({'message': 'fail to leave'}, status=200)

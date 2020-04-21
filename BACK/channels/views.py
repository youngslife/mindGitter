from django.shortcuts import render
from .models import Channel
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from .serializers import UserChannelSerializer, ChannelSerializer
import jwt
from django.http import JsonResponse
from back.settings import SECRET_KEY

# Create your views here.

# 채널 목록
@api_view(['GET', 'POST'])
def board(request):
    # jwt decode ## 후에 함수화
    try:
        token = request.headers.get('Authorization', None)[4:]
        payload = jwt.decode(token, SECRET_KEY, algorithm='HS256')

    except jwt.exceptions.DecodeError:
        return JsonResponse({'message': 'INVALID TOKEN'}, status=400)

    except User.DoesNotExist:
        return JsonResponse({'message': 'INVALID USER'}, status=400)

    username = payload['username']


    if request.method == 'GET': # list of diary books
        user = User.objects.get(username=username)
        serializers = UserChannelSerializer(user)
        return Response(serializers.data)

    elif request.method == 'POST':  # create a diary book
        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=username)
            channel = Channel.objects.last()
            user.channels.add(channel)
            return Response({'message': 'success to save'}, status=201)
        else:
            return Response({'message': 'fail to save'}, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def board_title(request, id):
    if request.method == 'GET': # channel detail
        channel = Channel.objects.get(id=id)
        serializer = ChannelSerializer(channel)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':  # update a channel
        channel = Channel.objects.get(id=id)
        serializer = ChannelSerializer(channel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success to update'}, status=201)
        else:
            return Response({'message': 'fail to update'}, status=400)

    elif request.method == 'DELETE':  # delete a channel
        channel = Channel.objects.get(id=id)
        channel.delete()
        return Response({'message': 'success to delete'}, status=200)
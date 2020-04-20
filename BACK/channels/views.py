from django.shortcuts import render
from .models import Channel
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from .serializers import UserChannelSerializer

# Create your views here.

# 채널 목록
@api_view(['GET'])
def board(request):
    username = request.query_params.get('username')
    user = User.objects.get(username=username)
    serializers = UserChannelSerializer(user)
    return Response(serializers.data)

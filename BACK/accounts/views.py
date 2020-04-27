from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserDisplaySerializer, ProfileImageSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import User


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

    def delete(self, request):
        profile_img = request.user.profile_img
        profile_img.delete()
        return Response(status=204)
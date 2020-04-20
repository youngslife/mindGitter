from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserDisplaySerializer
from rest_framework.permissions import IsAuthenticated

class CurrentUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = UserDisplaySerializer.profile_img(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data

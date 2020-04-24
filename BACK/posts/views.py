from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Tag, Emotion, Post, Comment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import CommentSerializer, TagSerializer, EmotionSerializer, PostSerializer
from accounts.models import User
from .models import Post
# 태구
from django.views.generic import ListView, DetailView, TemplateView


class PostList(APIView):
    permission_classes = (IsAuthenticated,)

    # 해당 user가 생성한 모든 post 조회
    def get(self, requet):
        # user-(channel)-post 연결후 만들기
        pass
    
    # post(일기) 생성
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = (IsAuthenticated,)

    # 조회
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        cover_img = post.cover_image
        cover_img.delete()
        video_file = post.video_file
        video_file.delete()
        serializer = PostSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, post_id):
        data = request.data.dict()
        data.update({'user': request.user.id})
        data.update({'post': post_id})
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'success to save comment'}, status=201)
        else:
            return JsonResponse({'message': serializer.errors }, status=400)

class CommentDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            data = request.data.dict()
            data.update({'user': request.user.id })
            data.update({'post': post_id})
            serializer = CommentSerializer(comment, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'success to save comment'}, status=200)
            else:
                # return JsonResponse({'message': 'fail to save comment'}, status=400)
                return JsonResponse({'message': serializer.errors}, status=400)
        else:
            return JsonResponse({'message': 'INVALID USER'}, status=400)


    def delete(self, reqeust, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == reqeust.user:
            posting = get_object_or_404(Post, id=post_id)
            if posting.comment_set.filter(id=comment_id).exists():
                comment.delete()
                return JsonResponse({'message': 'success to delete comment'}, status=200)
            else:
                return JsonResponse({'message': 'do not exists the comment in the post'}, status=400)
        else:
            return JsonResponse({'message': 'INVALID USER'}, status=400)
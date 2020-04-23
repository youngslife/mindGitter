from django.shortcuts import render, get_object_or_404
from .models import Tag, Emotion, Post, Comment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import CommentSerializer, TagSerializer, EmotionSerializer, PostSerializer
from accounts.models import User, UserTag
from .models import Post
# 태구
# from django.views.generic import ListView, DetailView, TemplateView

from accounts.serializers import UserTagSerializer
from taggit.models import TaggedItem





def usertag_update(request, user_id):
    
    user = get_object_or_404(User, pk=user_id)
    
    tags = request.data['tags']
    print('&&&&&&&&&&&&', tags)
    usertagSerializer = UserTagSerializer(instance=user, data={'tags': tags})
    if usertagSerializer.is_valid():
        print('!!!!!!!!!!!!!', usertagSerializer)
        usertagSerializer.save()
        return True
    return False

class PostList(APIView):
    permission_classes = (IsAuthenticated,)

    # 해당 user가 생성한 모든 post 조회
    def get(self, requet):
        # user-(channel)-post 연결후 만들기
        pass
    
    # post(일기) 생성
    # def post(self, request):
    #     user = get_object_or_404(User, username=request.user)
    #     serializer = PostSerializer(data=request.data)
    #     # user-tag serializer모르겠어서 for 문으로 저장
    #     if serializer.is_valid():
    #         # user = get_object_or_404(User, username=request.user)
    #         # print('***********', request.tags)
    #         serializer.save(user_id=user.id)
    #         posting = Post.objects.first()  # -pk 로 정렬이므로
    #         posting_id = posting.id
    #         taggeditem = TaggedItem.objects.filter(object_id=posting_id)
    #         for item in taggeditem:
    #             # print(item.tag_id)
    #             usertagSerializer = UserTagSerializer(data={'tag_id': item.tag_id})
    #             if usertagSerializer.is_valid():
    #                 usertagSerializer.save(user_id=user.id, tag_id=item.tag_id)
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = get_object_or_404(User, username=request.user)
        usertagSerializer = UserTagSerializer(data=request.data)
        if usertag_update(request, user.id):
            print('@@@@@@@@@@@@')
            # if usertagSerializer.is_valid():
            #     usertagSerializer.save()
            #     serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(usertagSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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



# 이 아래 부분은 구현하지 않음
# class Tag(APIView):
#     def post(self, request, format=None):
#         tags = request.query_params.get('hashtags', None)

#         if tags is not None:
#             tags = tags.split(',')
#             serialzer = TagSerializer





# def comment_list(request):
#     pass

# def comment_detail(request, id):
#     pass


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Tag, Emotion, Post, Comment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import CommentSerializer, TagSerializer, EmotionSerializer, PostSerializer
from accounts.models import User, UserTag
from .models import Post

from accounts.serializers import UserTagSerializer
from taggit.models import TaggedItem
# import json



# def usertag_update(request, user):
#     # print(type(request.data['tags']), request.data['tags'][:-1]) # json string list
#     new_tag = request.data['tags'][:-1]  # 새로 입력된 태그들 ["new", "hello"
#     temp_list = list(user.tags.all().values_list('name', flat=True))  # 원래 태그들 ['00', '111']
#     origin_tags = str(temp_list)[1:] # 원래 태그들
#     temp_tags = new_tag + ',' + origin_tags  # json list 태그 + 원래 태그들
#     tags = temp_tags.replace("'", "\"") # data에 담아줄 최종 json list
#     usertagSerializer = UserTagSerializer(instance=user, data={'tags': tags})
#     if usertagSerializer.is_valid():
#         usertagSerializer.save()
#         return True
#     return False


class PostList(APIView):
    permission_classes = (IsAuthenticated,)

    # 해당 user가 생성한 모든 post 조회
    def get(self, requet):
        # user-(channel)-post 연결후 만들기
        pass


    # post(일기) 생성
    def post(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = PostSerializer(data=request.data)
        # user-tag serializer모르겠어서 for 문으로 저장
        if serializer.is_valid():
            serializer.save(user_id=user.id)
            posting = Post.objects.first()  # -pk 로 정렬이므로
            posting_id = posting.id
            taggeditem = TaggedItem.objects.filter(object_id=posting_id)

            for item in taggeditem:
                if UserTag.objects.filter(tag_id=item.tag_id).exists():
                    continue
                usertagSerializer = UserTagSerializer(data={'tag_id': item.tag_id})
                if usertagSerializer.is_valid():
                    print('innnnnnnnnnn')
                    usertagSerializer.save(content_object_id=user.id, tag_id=item.tag_id)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # post(일기) 생성
    # def post(self, request):
    #     user = get_object_or_404(User, username=request.user)
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         if usertag_update(request, user): # 일기 생성시, user-tag update
    #             serializer.save(user_id=user.id)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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
        # print('###############원래 태그들', post.tags.all(), type(post.tags.all()))
        # print('요청 태그들', request.data.get('tags', None), type(request.data.get('tags', None)))
        # request_tags = request.data.get('tags', None)
        # update_tags =
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

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Tag, Emotion, Post, Comment
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import CommentSerializer, TagSerializer, EmotionSerializer, PostSerializer
from accounts.models import User, UserTag
from .models import Post
import json
from taggit.models import Tag
from accounts.serializers import UserTagSerializer
from taggit.models import TaggedItem

import requests

@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def tagtest(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    tags = post.tags.all()
    for tag in tags:
        print(tag.name, tag.weight)
    return Response()

class PostList(APIView):
    permission_classes = (IsAuthenticated,)

    # post(일기) 생성
    def post(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user_id=user.id, channel_id=request.data['channel_id'])
            
            ## AI 모델에 분석 요청 ===============================
            headers = {
                'Content-Type':'application/json'
            }
            data = {
                'video_url': 'https://mind-gitter-diary.s3.amazonaws.com/diary/' + request.data['video_file'],
                'post_id': str(Post.objects.first().id),
                'user_id': str(request.user.id)
            }
            res = requests.post('https://mind-gitter.me/message/', headers=headers, json=data)
            print(res)

            ## ==================================================

            posting = Post.objects.first()  # -pk 로 정렬이므로

            new_tags = posting.tags.names()
            for new_tag in new_tags:
                if user.tags.filter(name=new_tag).exists():
                    tag_id=user.tags.get(name=new_tag).id
                    usertag = UserTag.objects.get(tag=tag_id)
                    count = usertag.count
                    usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
                    if usertagserializer.is_valid():
                        usertagserializer.save(count=count+1)
                else:
                    user.tags.add(new_tag)

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class PostDetail(APIView):
    permission_classes = (IsAuthenticated,)

    # 조회
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # 수정
    def put(self, request, post_id):
        posting = get_object_or_404(Post, id=post_id)

        before_tags = posting.tags.names()
        for tag in before_tags:
            tag_id = get_object_or_404(Tag, name=tag).id
            usertag = get_object_or_404(UserTag, tag=tag_id)
            count = usertag.count
            usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
            print(usertagserializer)
            if usertagserializer.is_valid():
                usertagserializer.save(count=count-1)

        serializer = PostSerializer(instance=posting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_tags = posting.tags.names()
            user = posting.user
            for new_tag in update_tags:
                if user.tags.filter(name=new_tag).exists():
                    tag_id=user.tags.get(name=new_tag).id
                    usertag = UserTag.objects.get(tag=tag_id)
                    count = usertag.count
                    usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
                    if usertagserializer.is_valid():
                        usertagserializer.save(count=count+1)
                else:
                    user.tags.add(new_tag)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


## 모델 분석 결과 저장 요청 (요청은 모델 쪽에서)
class PostAnalyze(APIView):
    permission_classes = (AllowAny,)

    def put(self, request, post_id):
        
        posting = get_object_or_404(Post, id=post_id)
        origin_tags = list()
        tags = TaggedItem.objects.filter(object_id=post_id)
        for tag in tags:
            t = get_object_or_404(Tag, id=tag.tag_id)
            origin_tags.append(t.name)

        data = dict()
        data.update({'title': posting.title})
        data.update({'video_file': posting.video_file})
        data.update({'channel_id': posting.channel_id})
        data.update({'is_use_comment': posting.is_use_comment})
        data.update({'is_save_video': posting.is_save_video})
        data.update({'context': request.data.get('fulltext')[:999]})
        data.update({'csv_url': request.data.get('emotions')})
        data.update({'tags': request.data.get('tags')})
        data.update({'summary': request.data.get('abb')[:999]})
        data.update({'emotions': json.dumps(request.data.get('statistics'))})

        before_tags = posting.tags.names()
        # 원래 디비에 저장되어 있던 포스팅 태그들
        for tag in before_tags:
            tag_id = posting.user.tags.get(name=tag).id
            usertag = UserTag.objects.get(tag=tag_id)
            count = usertag.count
            usertagserializer = UserTagSerializer(instance=usertag, data=data)
            if usertagserializer.is_valid():
                usertagserializer.save(count=count-1)

        ## 태그 거르기
        temp = list()
        for tag in data.get('tags'):
            if ('/NNG' not in tag) and ('/NNB' not in tag):
                continue
            else:
                temp.append(tag[:-4])
        data.update({'tags': origin_tags + temp})
        

        serializer = PostSerializer(instance=posting, data=data)
        if serializer.is_valid():
            serializer.save()
            update_tags = posting.tags.names()
            user = posting.user
            for new_tag in update_tags:
                if user.tags.filter(name=new_tag).exists():
                    tag_id=user.tags.get(name=new_tag).id
                    usertag = UserTag.objects.get(tag=tag_id)
                    count = usertag.count
                    usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
                    if usertagserializer.is_valid():
                        usertagserializer.save(count=count+1)
                else:
                    user.tags.add(new_tag)
            return Response({'message': 'save to analyzed data in database successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, post_id):
        data = request.data
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
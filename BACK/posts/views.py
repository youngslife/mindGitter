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

from taggit.models import Tag

from accounts.serializers import UserTagSerializer
from taggit.models import TaggedItem


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

    # 해당 user가 생성한 모든 post 조회
    def get(self, requet):
        # user-(channel)-post 연결후 만들기
        pass


    # post(일기) 생성
    def post(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user.id, channel_id=request.data['channel_id'])         
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

            # 짧은 코드로 구현  법(3줄) => count 바꿀 수가 없음... / 수정 시, 문제 생김
            # new_tags = posting.tags.names()
            # for new_tag in new_tags:
            #     user.tags.add(new_tag)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        #파일이 아니라서 아래처럼 파일 지워줄 필요 없음 => 일단 혹시 몰라서 남겨둠
        # cover_img = post.cover_image
        # cover_img.delete()
        # video_file = post.video_file
        # video_file.delete()

        before_tags = posting.tags.names()
        # print('원래포스팅태그들', before_tags)
        for tag in before_tags:
            tag_id = posting.user.tags.get(name=tag).id
            usertag = UserTag.objects.get(tag=tag_id)
            count = usertag.count
            usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
            if usertagserializer.is_valid():
                usertagserializer.save(count=count-1)

        serializer = PostSerializer(instance=posting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_tags = posting.tags.names()
            # print('업데이트된 태그들', update_tags)
            # print('원래포스팅태그들', before_tags)
            user = posting.user
            for new_tag in update_tags:
                if user.tags.filter(name=new_tag).exists():
                    tag_id=user.tags.get(name=new_tag).id
                    # tag = Tag.objects.get(name=new_tag)
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


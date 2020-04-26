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
        # user-tag serializer모르겠어서 for 문으로 저장
        # inputtag = request.data.get('tags').split(",")
        # print('EEEEEEEEEEEEEEEEEE', inputtag)
        if serializer.is_valid():
            serializer.save(user_id=user.id, channel_id=request.data['channel_id'])         
            # inputtag =
            posting = Post.objects.first()  # -pk 로 정렬이므로
            
            
            new_tags = posting.tags.names()
            for new_tag in new_tags:
                if Tag.objects.filter(name=new_tag).exists():
                    tag= Tag.objects.get(name=new_tag)
                    usertag = UserTag.objects.get(tag_id=tag.id)
                    count = usertag.count
                    usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
                    if usertagserializer.is_valid():
                        usertagserializer.save(count=count+1)
                else:
                    user.tags.add(new_tag)

            # 짧은 코드로 구현  법(3줄) => count 바꿀 수가 없음...ㅠ
            # new_tags = posting.tags.names()
            # for new_tag in new_tags:
            #     user.tags.add(new_tag)


            # posting_id = posting.id
            # taggeditem = TaggedItem.objects.filter(object_id=posting_id)
            # print(taggeditem)
            # for item in taggeditem:
            #     # print('@@@@@@@', item.)
            #     if UserTag.objects.filter(tag_id=item.tag_id).exists():
            #         usertag = UserTag.objects.filter(tag_id=item.tag_id)
            #         count = usertag.count.
            #         print('######################', count)
            #         usertag.count.set(count+1)
            #         # usertag.count
            #         continue
            #     usertagSerializer = UserTagSerializer(data={'tag_id': item.tag_id})
            #     if usertagSerializer.is_valid():
            #         print('innnnnnnnnnn')
            #         usertagSerializer.save(content_object_id=user.id, tag_id=item.tag_id)
            #     else:
            #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:    
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
        posting = get_object_or_404(Post, id=post_id)
        #파일이 아니라서 아래처럼 파일 지워줄 필요 없음 => 일단 혹시 몰라서 남겨둠
        # cover_img = post.cover_image
        # cover_img.delete()
        # video_file = post.video_file
        # video_file.delete()
        # print('###############원래 태그들', post.tags.all(), type(post.tags.all()))
        # print('요청 태그들', request.data.get('tags', None), type(request.data.get('tags', None)))
        # request_tags = request.data.get('tags', None)
        # update_tags =
        before_tags = posting.tags.names()
        print('원래포스팅태그들', before_tags) # [태그, 헤헤]
        serializer = PostSerializer(instance=posting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_tags = posting.tags.names() # [헤헤, 삼태]
            print('업데이트된 태그들', update_tags)
            user = posting.user
            
            # usertag = UserTag.objects.filter(content_object_id=posting.user_id)
            # print('해당 user의 모든 태그들 연결된 테이블 객체들', tags_in_user) # [1, 2, 3]객체들
            for tag in update_tags:
                if tag not in before_tags:
                    user.tags.add(tag) 
                    # tagobject = Tag.objects.get(name=tag)
                    # print('!!!!!!!!!!!!!!!!!!!!!', tagobject.id)
                    # if UserTag.objects.filter(tag_id=tagobject.id).exists():
                    #     usertag = UserTag.objects.get(tag_id=tagobject.id)
                    #     print('#@#%#$@%$!#%!@#', usertag)
                    #     count = usertag.count
                    #     usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
                    #     if usertagserializer.is_valid():
                    #         usertagserializer.save(count=count-1)
                    # else:
                    #     print('aeiwlg;lqawehg;ljwae;oil')
                    #     user.tags.add(tag)

                # else:
                #     print('**********************')
                #     user.tags.add(tag)      

            for tag in before_tags:
                if tag not in update_tags:
                    # user.tags.remove(tag)
                    tagobject = Tag.objects.get(name=tag)
                    print('!!!!!!!!!!!!!!!!!!!!!', tagobject.id)
                    if UserTag.objects.filter(tag_id=tagobject.id).exists():
                        usertag = UserTag.objects.get(tag_id=tagobject.id)
                        print('#@#%#$@%$!#%!@#', usertag)
                        count = usertag.count
                        usertagserializer = UserTagSerializer(instance=usertag, data=request.data)
                        if usertagserializer.is_valid():
                            usertagserializer.save(count=count-1)
            
            

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

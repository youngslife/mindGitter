from rest_framework import serializers
from .models import Post, Emotion, Tag, Comment
from accounts.models import User, UserEmotion
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
# from accounts.serializers import UserTagSerializer, UserDisplaySerializer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    # comments = PostCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Tag
        fields = '__all__'


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = '__all__'

# for calendar filtering
class PostDateFilterSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        today = datetime.now()
        six_months_ago = today + relativedelta(months=-6)
        data = data.filter(created_at__lte=today).filter(created_at__gte=six_months_ago)
        if data:
            first_p = data[0]
            list_post_created = [{ first_p.created_at.strftime('%Y-%m-%d'): [first_p.id] }]

            for posting in data[1:]: # 각 포스트 데이터
                ddate = posting.created_at.strftime('%Y-%m-%d')
                for post_created in list_post_created:
                    if ddate in post_created.keys():
                        post_created[ddate].append(posting.id); break
                    else:
                        list_post_created.append({ddate: [posting.id]}); break

            return list_post_created
        else:
            return super(PostDateFilterSerializer, self).to_representation(data)


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    comment_set = CommentSerializer(read_only=True, many=True)
    tags = TagListSerializerField()
    class Meta:
        list_serializer_class = PostDateFilterSerializer
        model = Post
        fields = ('pk', 'title', 'cover_image', 'user_id',
                    'context', 'created_at', 'updated_at', 
                    'video_file', 'tags', 'comment_set', 'channel_id', )   

   
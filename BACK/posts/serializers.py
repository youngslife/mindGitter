from rest_framework import serializers
from .models import Post, Emotion, Tag, Comment
from accounts.models import User, UserEmotion
# from accounts.serializers import UserDisplaySerializer
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
# from accounts.serializers import UserDisplaySerializer
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
        
        return super(PostDateFilterSerializer, self).to_representation(data)


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    comment_set = CommentSerializer(read_only=True, many=True)
    tags = TagListSerializerField()
    # user_set = UserDisplaySerializer(read_only=True)

    # def to_representation(self, instance):
    #     self.fields['user'] = UserDisplaySerializer(read_only=True)
    #     return super(PostSerializer, self).to_representation(instance)

    class Meta:
        model = Post
        fields = ('pk', 'title', 'video_file', 'context', 'emotion', 'summary', 'tags',
        'created_at', 'updated_at', 'channel_id', 'user_id', 'comment_set',
        'is_use_comment', 'is_save_video')

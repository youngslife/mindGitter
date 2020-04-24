from rest_framework import serializers
from .models import Post, Emotion, Tag, Comment
from accounts.models import User, UserEmotion
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
from accounts.serializers import UserTagSerializer, UserDisplaySerializer


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


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    # comments = CommentSerializer(many=True)
    tags = TagListSerializerField()
    # user_id = UserTagSerializer()
    # user_id = UserDisplaySerializer()
    # emotions = EmotionSerializer(many=True)
    # Channel 은 일단 생략
    # channel_id = 1git
    class Meta:
        model = Post
        fields = ('pk', 'title', 'cover_image', 'user_id',
                    'context', 'created_at', 'updated_at', 
                    'video_file', 'tags', )   

   
from rest_framework import serializers
from accounts.models import User, UserTag
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)

from django.contrib.contenttypes.models import ContentType

class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", )


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_img"]


class UserTagSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = User
        fields = ('pk', 'tags',)


# class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
#     # comments = CommentSerializer(many=True)
#     tags = TagListSerializerField()
#     # emotions = EmotionSerializer(many=True)
#     # Channel 은 일단 생략
#     # channel_id = 1git
#     class Meta:
#         model = Post
#         fields = ('pk', 'title', 'cover_image',
#                     'context', 'created_at', 'updated_at', 'video_file', 'tags',)   

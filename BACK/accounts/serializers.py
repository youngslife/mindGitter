from rest_framework import serializers
from accounts.models import User, UserTag, Notification
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
from posts.serializers import PostSerializer
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
    post_set = PostSerializer(many=True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_img", "post_set", )


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_img"]


class UserTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTag
        fields = ('content_object_id', 'tag_id', 'count')


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

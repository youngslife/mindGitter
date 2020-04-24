from rest_framework import serializers
from .models import Channel
from accounts.models import User
from accounts.serializers import UserDisplaySerializer
from posts.serializers import PostSerializer
from datetime import datetime
import json


class ChannelSerializer(serializers.ModelSerializer):
    user_set = UserDisplaySerializer(read_only=True, many=True)
    post_set = PostSerializer(read_only=True, many=True)

    def to_representation(self, instance):
        self.fields['create_user'] = UserDisplaySerializer(read_only=True)
        return super(ChannelSerializer, self).to_representation(instance)

    class Meta:
        model = Channel
        fields = '__all__'


class UserChannelSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True)

    class Meta:
        model = User
        fields = ('pk', 'username', 'channels',)

# after making post serializer


class ChannelPostSerializer(ChannelSerializer):
    pass

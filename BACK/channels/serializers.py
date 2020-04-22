from rest_framework import serializers
from .models import Channel
from accounts.models import User
from accounts.serializers import UserDisplaySerializer
from datetime import datetime
import json


class ChannelSerializer(serializers.ModelSerializer):
    # create_user = UserDisplaySerializer()
    # users = UserDisplaySerializer(source='user_set', many=True)

    def create_user(self):
        self.create_user = UserDisplaySerializer()

    def users(self):
        self.users = UserDisplaySerializer(source='user_set', many=True)

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

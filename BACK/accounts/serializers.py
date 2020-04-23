from rest_framework import serializers
from accounts.models import User
# from channels.serializers import ChannelSerializer


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", )


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_img"]
from rest_framework import serializers
from accounts.models import User
from channels.serializers import ChannelSerializer


class UserDisplaySerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(allow_empty_file=True, default='../media/user/default_profile.png')
    
    class Meta:
        model = User
        fields = ("username", "email", "profile_img", )


# class ProfileImageSerializer(serializers.ModelSerial)

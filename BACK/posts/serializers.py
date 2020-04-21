# from rest_framework import serializers
# from .models import Post, Emotion, Tag, Comment
# from accounts.models import User


# class PostDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Channel
#         fields = '__all__'


# class UserPostSerializer(ChannelSerializer):
#     channels = ChannelSerializer(many=True)

#     class Meta:
#         model = User
#         fields = ('pk', 'username', 'channels',)

# # after making post serializer
# class PostCommentSerializer
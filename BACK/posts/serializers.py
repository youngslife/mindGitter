# from rest_framework import serializers
# from .models import Post, Emotion, Tag, Comment
# from accounts.models import User, UserEmotion


# class PostCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'


# class PostSerializer(serializers.ModelSerializer):
#     comments = PostCommentSerializer(many=True, read_only=True)
#     class Meta:
#         model = Post
#         fields = '__all__'


# class UserPostSerializer(PostSerializer):
#     post=PostSerializer(many=True)

#     class Meta:
#         model = User
#         fields = ('pk', 'username', 'channels',)



    
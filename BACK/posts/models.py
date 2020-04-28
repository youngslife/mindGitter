from django.db import models
from django.conf import settings
from channels.models import Channel
from taggit.managers import TaggableManager
# Tag-usr 중간테이블만들기
# from taggit.models import TaggedItemBase
# from accounts.models import User

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

class Emotion(models.Model):
    category = models.CharField(max_length=20)



class Post(models.Model):
    title = models.CharField(max_length=50)
    cover_image = models.CharField(max_length=100)
    context = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # channel blank=True 지워야함!1!!!연결안해놔서 테스트할려구 해둔거임
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    emotions = models.ManyToManyField(Emotion, blank=True)
    video_file = models.CharField(max_length=100)
    # summary = models.CharField(max_length=200)
    # use_comment = models.BooleanField()
    # save_video = models.BooleanField()

    class Meta:
        ordering = ['-pk']
    def __str__(self):
        return self.title
        
class Comment(models.Model):
    context = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
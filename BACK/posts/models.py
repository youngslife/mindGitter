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
    video_file = models.CharField(max_length=100)
    context = models.CharField(max_length=200, blank=True)
    # emotions 분석 결과는 csv 파일에서 직접 확인하게 됨으로써
    # manytomany가 아닌 csv의 s3 url로 저장 후 프론트에 전달, 따라서 char field로 변경
    emotion = models.CharField(max_length=200, blank=True)
    summary = models.CharField(max_length=200, blank=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_use_comment = models.BooleanField() # 코멘트 허용 여부
    is_save_video = models.BooleanField() # 영상 저장 여부
    # 후에 cover_image 삭제
    # cover_image = models.CharField(max_length=100)
    # emotions = models.ManyToManyField(Emotion, blank=True)

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
    class Meta:
        ordering = ['-pk']
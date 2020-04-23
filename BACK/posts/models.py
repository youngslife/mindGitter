from django.db import models
from django.conf import settings
from channels.models import Channel
from taggit.managers import TaggableManager

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

class Emotion(models.Model):
    category = models.CharField(max_length=20)



class Post(models.Model):
    title = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to="post/%Y/%m/%d/cover/", blank=True)
    context = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    emotions = models.ManyToManyField(Emotion, blank=True)
    video_file = models.FileField(upload_to='post/%Y/%m/%d/video/', blank=True)
    # summary = models.CharField(max_length=200)

    class Meta:
        ordering = ['-pk']
    def __str__(self):
        return self.title
        
class Comment(models.Model):
    context = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
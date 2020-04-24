from django.db import models
from django.conf import settings
from channels.models import Channel

# Create your models here.
class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

class Emotion(models.Model):
    category = models.CharField(max_length=20)

class Post(models.Model):
    title = models.CharField(max_length=50)
    cover_image = models.CharField(max_length=100)
    context = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    emotions = models.ManyToManyField(Emotion, blank=True)
    
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
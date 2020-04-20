from django.db import models
from django.contrib.auth.models import AbstractUser
from channels.models import Channel
from posts.models import Tag, Emotion


# Create your models here.
class User(AbstractUser):
    channels = models.ManyToManyField(Channel, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    emotions = models.ManyToManyField(Emotion, blank=True)
    
    profile_img = models.ImageField(upload_to='user', blank=True, default='../media/user/default_profile.png')

    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return self.username
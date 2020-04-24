from django.db import models
from django.conf import settings

# Create your models here.


class Channel(models.Model):
    title = models.CharField(max_length=50)
    cover_image = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

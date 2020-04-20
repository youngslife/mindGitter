from django.db import models

# Create your models here.
class Channel(models.Model):
    title = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to="image")
    discription = models.CharField(max_length=200)

    def __str__(self):
        return self.title
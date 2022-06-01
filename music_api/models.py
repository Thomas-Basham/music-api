from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Music(models.Model):
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.TextField()
    artist = models.TextField()
    # image = models.CharField(max_length=600, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIS9NmMDZNSiXrq6Q1C62ihL3MuLsXLfUw2w&usqp=CAU', null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='media/')
    # audio_file = models.FileField(blank=True,null=True)
    audio_link = models.CharField(max_length=200,blank=True,null=True)
    duration = models.CharField(max_length=20)
    paginate_by = 2

    def __str__(self):
        return self.title

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import cloudinary
from cloudinary.models import CloudinaryField
import cloudinary.uploader


def validate_file_size(value):
    filesize = value.size

    if filesize > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


# Create your models here.
class Music(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=64)
    artist = models.CharField(max_length=64)
    img = CloudinaryField('img', null=True)
    audio = CloudinaryField('audio', resource_type="video", null=True)
    paginate_by = 2
    plays = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("music_list_api")

    def increment(self):
        self.plays += 1
        self.save()

@receiver(pre_delete, sender=Music)
def photo_delete(sender, instance, **kwargs):
    if instance.audio or instance.img:
        cloudinary.uploader.destroy(instance.audio.public_id, resource_type="video")
        cloudinary.uploader.destroy(instance.img.public_id)


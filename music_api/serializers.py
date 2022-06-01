from rest_framework import serializers
from .models import Music


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "added_by", "title", "artist", "image", "audio_link", "duration", "paginate_by")
        model = Music

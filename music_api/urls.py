from django.urls import path
from .views import MusicList, MusicDetail, index

urlpatterns = [
    path("", MusicList.as_view(), name="music_list"),
    path("player/", index, name="music_list"),
    path("<int:pk>/", MusicDetail.as_view(), name="music_detail"),
]

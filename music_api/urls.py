from django.urls import path
from .views import MusicList, MusicDetail, index

urlpatterns = [
    path("", index, name="music_list"),
    path("admin/", MusicList.as_view(), name="music_list"),
    path("<int:pk>/", MusicDetail.as_view(), name="music_detail"),
]

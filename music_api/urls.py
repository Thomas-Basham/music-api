from django.urls import path

from .views import MusicListCreateView, MusicRetrieveUpdateDestroyView

urlpatterns = [
  path("music/", MusicListCreateView.as_view(), name="music_list"),
  path("music/<int:pk>/", MusicRetrieveUpdateDestroyView.as_view(), name="music_detail"),
]

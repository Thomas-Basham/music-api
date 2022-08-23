from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Music


class MusicTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_music = Music.objects.create(
            title="Three Little Birds",
            added_by=testuser1,
            artist="Bob Marley",
        )
        test_music.save()

    # class 32
    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_musics_model(self):
        music = Music.objects.get(id=1)
        actual_owner = str(music.added_by)
        actual_name = str(music.title)
        actual_description = str(music.artist)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "Three Little Birds")
        self.assertEqual(
            actual_description, "Bob Marley"
        )

    def test_get_music_list(self):
        url = reverse("music_list_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        musics = response.data
        self.assertEqual(len(musics), 1)
        self.assertEqual(musics[0]["title"], "Three Little Birds")

    def test_get_music_by_id(self):
        url = reverse("music_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        music = response.data
        self.assertEqual(music["title"], "Three Little Birds")

    def test_create_music(self):
        url = reverse("music_list_api")
        data = {"owner": 1, "title": "Like A stone", "artist": "Audioslave"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        musics = Music.objects.all()
        self.assertEqual(len(musics), 2)
        self.assertEqual(Music.objects.get(id=2).title, "Like A stone")

    def test_update_music(self):
        url = reverse("music_detail", args=(1,))
        data = {
            "added_by": 1,
            "title": "Three Little Birds",
            "artist": "Bob Marley",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        music = Music.objects.get(id=1)
        self.assertEqual(music.title, data["title"])
        self.assertEqual(music.added_by.id, data["added_by"])
        self.assertEqual(music.artist, data["artist"])

    def test_delete_music(self):
        url = reverse("music_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        musics = Music.objects.all()
        self.assertEqual(len(musics), 0)

    # class 33
    def test_authentication_required(self):
        self.client.logout()
        url = reverse("music_list_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

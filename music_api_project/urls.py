"""music_api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.views import SpectacularAPIView
from music_api.views import SongCreate, \
  register_request, login_request, logout_request, index

urlpatterns = [
  # Back End
  path('api/v1/music/', include('music_api.urls')),
  path("admin/", admin.site.urls),
  path('api/', SpectacularAPIView.as_view(), name='schema'),
  path("api-auth/", include("rest_framework.urls")),
  path(
    "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
  ),
  path(
    "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
  ),

  # Front End
  path("", index, name="index"),
  path("register", register_request, name="register"),
  path("login", login_request, name="login"),
  path("logout", logout_request, name="logout"),
  path("add-song-form", SongCreate.as_view(), name="add_song_form"),
  path('documentation/', TemplateView.as_view(
    template_name='swagger-ui.html',
    extra_context={'schema_url': 'schema'}
    # assuming `request` is available here}}
  ), name='swagger-ui'),
]

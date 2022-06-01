from rest_framework import generics
from .models import Music
from .permissions import IsOwnerOrReadOnly
from .serializers import MusicSerializer


class MusicList(generics.ListCreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class MusicDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

# Create your views here.
from django.shortcuts import render, redirect

# imported our models
from django.core.paginator import Paginator
from . models import Music


def index(request):
    paginator= Paginator(Music.objects.all(),1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request,"index.html",context)
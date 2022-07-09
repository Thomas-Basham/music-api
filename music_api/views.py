from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.views.generic.edit import CreateView
from .forms import NewUserForm
from .permissions import IsOwnerOrReadOnly
from .serializers import MusicSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
# import models
from .models import Music


class MusicList(generics.ListCreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class MusicDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


def index(request):
    paginator = Paginator(list(reversed(Music.objects.all())), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = dict(page_obj=page_obj)
    context["dataset"] = Music.objects.all().order_by("-id")

    return render(request, "index.html", context)


class SongCreate(CreateView):
    model = Music
    fields = ["title", "artist", "img", "audio"] # "added_by",
    # fields = "__all__"
    success_url = reverse_lazy('index')

    # https://developpaper.com/file-upload-in-django-using-class-based-view/
    # Remove CSRF protection temporarily, don't learn from me!
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SongCreate, self).dispatch(request, *args, **kwargs)

    # override
    def form_valid(self, form):
        # Add the user object into the form and store it in the model
        form.instance.added_by = self.request.user
        return super(SongCreate, self).form_valid(form)


class SongForm(ModelForm):
    class Meta:
        model = Music
        fields = "__all__"

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")

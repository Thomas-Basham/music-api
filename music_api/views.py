from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, renderers, schemas
from django.views.generic.edit import CreateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator

from .forms import NewUserForm
from .serializers import MusicSerializer
from .models import Music
from .permissions import IsOwnerOrReadOnly


class MusicListCreateView(generics.ListCreateAPIView):
  queryset = Music.objects.all()
  serializer_class = MusicSerializer
  permission_classes = [IsOwnerOrReadOnly]


class MusicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Music.objects.all()
  serializer_class = MusicSerializer
  permission_classes = [IsOwnerOrReadOnly]


@api_view
@renderer_classes([renderers.OpenAPIRenderer])
def schema_view(request):
  generator = schemas.SchemaGenerator(title='Music API')
  return Response(generator.get_schema())


def index(request):
  paginator = Paginator(list(reversed(Music.objects.all())), 1)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  if page_obj.has_next():
    next_page = paginator.get_page(page_obj.next_page_number())
  if not page_obj.has_next():
    next_page = paginator.get_page('1')
  if page_obj.has_previous():
    prev_page = paginator.get_page(page_obj.previous_page_number())
  if not page_obj.has_previous():
    prev_page = paginator.get_page('-1')
  context = dict()
  context["page_obj_item"] = page_obj[0]
  context["page_obj"] = page_obj
  context["songs"] = list(reversed(Music.objects.all()))
  context["next_page"] = next_page[0]
  context["prev_page"] = prev_page[0]
  context["end_page"] = paginator.get_page('-1')
  context['song_played'] = False
  return render(request, "index.html", context)


class SongCreate(CreateView):
  model = Music
  fields = ["title", "artist", "img", "audio"]  # "added_by",
  success_url = reverse_lazy('index')

  # https://developpaper.com/file-upload-in-django-using-class-based-view/
  # Remove CSRF protection temporarily, don't learn from me!
  @csrf_exempt
  def dispatch(self, request, *args, **kwargs):
    return super(SongCreate, self).dispatch(request, *args, **kwargs)

  # override
  def form_valid(self, form):
    # Add the user object into the form and store it in the model
    if self.request.user:
      form.instance.added_by = self.request.user
    else:
      form.instance.added_by = None
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


def documentation(request):
  context = dict(current_user=request.user)
  return render(request, 'documentation.html', context)

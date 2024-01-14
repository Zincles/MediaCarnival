from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from core.models import MediaLibrary, FSNode


def blank(request):
    return render(request, "image_viewer/blank.html")

# Create your views here.
def image_viewer(request, image_path):
    return render(request, "image_viewer/image_viewer.html", {"image_path": image_path})

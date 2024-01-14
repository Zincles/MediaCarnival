from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from core.models import MediaLibrary, FSNode
import os

def home(request):
    return render(request, "image_viewer/home.html")

# Create your views here.
def image_viewer(request, image_path):
    
    IMAGE_PATH = os.path.join("/", image_path)
    os.system("echo $PATH")  
    return render(request, "image_viewer/image_viewer.html", {"IMAGE_PATH": IMAGE_PATH})


# 读取图像文件并返回HTTP Response.
def load_image(request, image_path):
    IMAGE_PATH = os.path.join("/", image_path)
    with open(IMAGE_PATH, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")  
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from core.models import MediaLibrary, FSNode


def home(request):
    return render(
        request,
        "media_library/home.html",
        {
            "file_paths": [
                "/home/zincles/TestCase/1.txt",
                "/home/zincles/TestCase/TEST CASE.txt",
                "/home/zincles/TestCase/VIDEO.mp4",
                "/home/zincles/TestCase/TEXT.txt",
            ],
        },
    )


def libraries(request):
    # 访问所有的库。
    all_library = list(MediaLibrary.objects.all())
    return render(
        request,
        "media_library/libraries.html",
        {"LIBRARIES": all_library},
    )


def library_inspector(request, library_id):
    # 访问具体的某个媒体库，查看里面的内容。
    # 在Jellyfin里，等价于“进入某个节目中”，大概

    return render(request, "media_library/library_inspector.html", {})

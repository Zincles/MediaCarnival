from django.http import HttpResponse
from django.shortcuts import render
import os
import json
from lib.extlib import get_file_type
import json


def home(request):
    if request.user.is_anonymous:
        return render(request, "file_browser/home.html")
    else:
        favorate_paths :dict= request.user.user_config.favorite_paths
        return render(
            request,
            "file_browser/home.html",
            {
                "favorate_paths": (favorate_paths)
            },
        )


def file_browser(request, path=""):
    path = os.path.join("/", path)  # 待遍历文件夹

    if os.path.isdir(path):
        raws = os.listdir(path)
        raws = sorted(raws, key=lambda x: x.lower())  # 对raws进行按名称从A-Z, a-z的排序

        name = os.path.basename(path)  # 所在目录的名称

        return render(
            request,
            "file_browser/file_browser.html",
            {
                "path": path,
                "name": name,
                "display_column": request.user.user_config.file_browser_cols if not request.user.is_anonymous else 4,
            },
        )

    elif os.path.isfile(path):
        return file_inspector(request, path)
    else:
        return HttpResponse("This is not a file or folder:" + str(path))


def file_inspector(request, path=""):
    """
    文件检查器, 用于检查文件的内容, 以及文件的编码格式
    file_browser可用于浏览目录，但是不可用于查看文件内容。file_inspector可用于查看文件内容，提供预览
    具体访问文件 会使用其他API
    """
    path = os.path.join("/", path)  # 待遍历文件夹

    if os.path.isdir(path):
        return HttpResponse("This is a Folder:" + str(path))
    elif not os.path.isfile(path):
        return HttpResponse("This is not a file or folder:" + str(path))
    else:
        with open(path, "rb") as f:
            content = f.read()
            return render(
                request,
                "file_browser/file_inspector.html",
                {
                    "path": path,
                    "name": os.path.basename(path),
                    "type": get_file_type(path),
                },
            )

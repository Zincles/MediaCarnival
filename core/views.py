from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
import os


#  返回文件系统中的文件
#  TODO 该方法极其危险！可能会泄漏你电脑上的文件。之后得做好鉴权相关工作才行。
@login_required
def file(request, path: str):
    if path[0] == "/":  # 绝对路径
        IMAGE_PATH = path
    else:  # 相对MediaCarnival根目录的路径
        # IMAGE_PATH = os.path.join(__file__, os.pardir, os.pardir, path)
        IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)

    print(f"处理后图像绝对路径:{IMAGE_PATH}")

    file_extension = os.path.splitext(path)[1]  # 该函数能够返回文件的扩展名

    match file_extension:
        case ".svg":
            with open(IMAGE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/svg+xml")
        case ".png":
            with open(IMAGE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/png")
        case ".jpg":
            with open(IMAGE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpg")
        case ".jpeg":
            with open(IMAGE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        case ".webp":
            with open(IMAGE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/webp")
        case _:
            with open(IMAGE_PATH, "rb") as f:
                return HttpResponse(f.read())
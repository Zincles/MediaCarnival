from django.http import Http404, HttpResponse
from django.shortcuts import render
import os
import json


## 获取图像文件
def api_get_image(request, path: str):

    FILE_PATH = os.path.join("/", path)

    # 检查FILE_PATH是否有效
    if not os.path.isfile(FILE_PATH):
        return HttpResponse("File not found at: <br>" + str(FILE_PATH))
    
    print(FILE_PATH)
    print("\n")

    file_extension = os.path.splitext(FILE_PATH)[1]  # 该函数能够返回文件的扩展名
    match file_extension:
        case ".svg":
            with open(FILE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/svg+xml")
        case ".png":
            with open(FILE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/png")
        case ".jpg":
            with open(FILE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpg")
        case ".jpeg":
            with open(FILE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        case ".webp":
            with open(FILE_PATH, "rb") as f:
                return HttpResponse(f.read(), content_type="image/webp")
        case _:
            return Http404("Not a Image file, or image format not supported")
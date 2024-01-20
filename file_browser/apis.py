from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
import os
import json


## 获取文件夹下的所有文件与文件夹。可指定页数，每页的数量，排序方式，排序顺序
def api_get_folder(request, path: str):
    
    # 获取查询参数
    page:int = request.GET.get("page", 1) 
    page_size:int = request.GET.get("page_size", 100)  
    sort = request.GET.get("sort", "name")
    order = request.GET.get("order", "asc")

    path: str = os.path.join("/", path)  # 待遍历文件夹
    name: str = os.path.basename(path)  # 所在目录的名称

    if os.path.isdir(path):
        # 处理names， 对names排序，按A-Z, a-z的顺序，文件夹在先，文件在后
        _names = os.listdir(path)
        _names.sort(key=lambda x: x.lower())
        _names.sort(key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)

        # 分页. 从第page页开始，每页page_size个。
        paginator = Paginator(_names, page_size)

        
        # 如果请求的页数超过了总页数，返回一个空的响应
        if int(page) > int(paginator.num_pages):
            return HttpResponse(
                json.dumps({
                    "names": [],
                    "paths": [],
                    "types": [],
                    "is_end": True
                })
            )
        
        
        
        names = paginator.get_page(page).object_list
        is_end = not paginator.page(page).has_next()

        paths = [os.path.join(path, name) for name in names]
        types = ["folder" if os.path.isdir(path) else "file" for path in paths]

        return HttpResponse(
            json.dumps(
                {
                    "page": page,  # 当前页码
                    "page_size": page_size,  # 每页的数量
                    "sort": sort,  # 排序方式
                    "order": order,  # 排序顺序
                    "path": path,  # 当前目录
                    "paths": paths,  # 当前目录下的所有文件与文件夹的路径
                    "name": name,  # 当前目录的名称
                    "names": names,  # 当前目录下的所有文件与文件夹的名称
                    "types": types,  # 当前目录下的所有文件与文件夹的类型
                    "is_end": is_end,  # 是否到达最后一页
                }
            )
        )
    else:
        return HttpResponse("Not a folder" + str(path))


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

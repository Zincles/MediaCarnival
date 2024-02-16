#   ALL CODE WRITTEN BY Down Zincles, Following GPLv3 Lisence.
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import Http404, HttpResponse, FileResponse
from .models import UserConfig, Thumbnail, MediaLibrary
from .lib import extlib
import os, json


def api_get_folder(request):
    """获取文件夹下的所有文件与文件夹。可指定页数，每页的数量，排序方式，排序顺序。"""

    # 获取查询参数
    path: str = os.path.join("/", request.GET.get("path", "/"))  # 待遍历文件夹
    page: int = request.GET.get("page", 1)  # 当前页数
    page_size: int = request.GET.get("pageSize", 100)  # 总共页数
    sort: str = request.GET.get("sort", "name")  # 排序方式

    def sort_arr(arr: list, method="name"):
        """对容纳了文件名的字符串数组进行排序。"""
        match method:
            case "name":
                arr.sort(key=lambda x: x.lower())
                arr.sort(key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)
            case "time":
                arr.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
                arr.sort(key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)
            case _:
                arr.sort(key=lambda x: x.lower())
                arr.sort(key=lambda x: os.path.isdir(os.path.join(path, x)), reverse=True)

    # 只有文件夹才能被遍历
    if os.path.isdir(path):
        raw_names = os.listdir(path)  # 处理文件名称， 对names排序，按A-Z, a-z的顺序，文件夹在先，文件在后
        sort_arr(raw_names, sort)

        paginator = Paginator(raw_names, page_size)  # 分页

        if int(page) > paginator.num_pages:  # 检查请求的页数是否超出实际页数
            names = []
        else:
            names = [i for i in paginator.get_page(int(page))]

        is_end = int(page) >= paginator.num_pages

        # 创建API返回的数组
        sub_paths: list[dict] = [
            {
                "path": os.path.join(path, name),
                "basename": name,
                "type": extlib.get_file_type(os.path.join(path, name)),
                "index": (int(page) - 1) * int(page_size) + index,  # Index. 计算得到. 有些危险.
            }
            for index, name in enumerate(names)  # 用name遍历
        ]

        return HttpResponse(
            json.dumps(
                {
                    "page": page,  # 当前页码
                    "pageSize": page_size,  # 每页的数量
                    "totalPages": paginator.num_pages,  # 总页数
                    "totalDirs": len(raw_names),  # 总文件数(非单页)
                    "isEnd": is_end,  # 是否到达最后一页
                    "subPaths": sub_paths,  # 当前目录下的子目录（文件/文件夹）
                }
            )
        )
    else:
        return Http404("Not a folder" + str(path))


def get_file_preview(request, path: str):
    """获取可预览文件的预览. 视频,音频,文本,pdf,诸如此类"""
    path = os.path.join("/", path)  # 确保是绝对路径

    # 检查FILE_PATH是否对应文件
    if not os.path.isfile(path):
        return HttpResponse("File not found at: <br>" + str(path))

    ext = extlib.get_ext_no_dot(path)

    # 根据文件类型，返回不同的响应
    match extlib.get_file_type(path):
        case "video":
            response = FileResponse(open(path, "rb"), content_type=f"video/{ext}")
            response["Accept-Ranges"] = "bytes"
            return response
        case "audio":
            response = FileResponse(open(path, "rb"), content_type=f"audio/{ext}")
            response["Accept-Ranges"] = "bytes"
            return response
        case "text":
            response = FileResponse(open(path, "rb"), content_type=f"text/{ext}")
            response["Accept-Ranges"] = "bytes"
            return response
        case "pdf":
            response = FileResponse(open(path, "rb"), content_type="application/pdf")
            response["Accept-Ranges"] = "bytes"
            return response
        case "image":
            response = FileResponse(open(path, "rb"), content_type=f"image/{ext}")
            response["Accept-Ranges"] = "bytes"
            return response
        case _:
            return HttpResponse("Preview not supported for this file type")


def get_user_config(request):
    """获取用户的当前配置。返回JSON格式。"""
    user_config: UserConfig = request.user.user_config
    return HttpResponse(json.dumps(user_config.__dict__))


def get_media_libraries(request):
    """
    获取所有的媒体库。返回JSON格式。
    {libraries:[{Library1}, {Library2}, {...}]}
    """
    
    libraries = [model_to_dict(lib, ["id", "library_name"]) for lib in MediaLibrary.objects.all()]
    return HttpResponse(json.dumps({"libraries": libraries}))


def get_media_library_by_id(request):
    """根据ID获取媒体库。"""
    library_id = request.GET.get("library_id")
    return HttpResponse(f"OK, id is {library_id}")
    return MediaLibrary.objects.get_or_create(site_id=1)[0]

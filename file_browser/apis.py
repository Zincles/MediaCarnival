from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from file_browser.models import Thumbnail
from lib import extlib
import os
import json


## 获取文件夹下的所有文件与文件夹。可指定页数，每页的数量，排序方式，排序顺序
def api_get_folder(request):
    # 获取查询参数
    path: str = os.path.join("/", request.GET.get("path", "/"))  # 待遍历文件夹
    page: int = request.GET.get("page", 1)  # 当前页数
    page_size: int = request.GET.get("pageSize", 100)  # 总共页数
    sort: str = request.GET.get("sort", "name")  # 排序方式

    ## 对（文件名）数组进行排序
    def sort_arr(arr: list, method="name"):
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

        # 检查请求的页数是否超出实际页数
        if int(page) > paginator.num_pages:
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
                "index": (int(page) - 1) * int(page_size) + index, # Index. 计算得到. 有些危险.
            }
            for index, name in enumerate(names)  # 用name遍历
        ]

        # print("Path:",path)
        # print("OS:",os.listdir(path))
        # print("Names:",names)
        # print("subPATHS:",sub_paths)

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


## TODO BROKEN
import pysubs2
import webvtt
from datetime import timedelta


def ms_to_timestamp(ms):
    seconds, milliseconds = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def convert_ass_to_vtt(ass_path):
    subs = pysubs2.load(ass_path, encoding="utf-8")
    vtt = webvtt.WebVTT()
    for sub in subs:
        start = ms_to_timestamp(sub.start)
        end = ms_to_timestamp(sub.end)
        text = sub.text.replace("\\N", "\n")
        vtt.captions.append(webvtt.Caption(start, end, text))
    return str(vtt)


## TODO 字幕转换功能仍然是坏的，需要修复。FIXME
## 引入的两个库：pysubs2 webvtt-py， 有可能有问题。
## 字幕的可用性并不高，需要完善。
def get_subtitle(request, video_path: str):
    video_path = os.path.join("/", video_path)
    base_path = os.path.splitext(video_path)[0]
    subtitle_path = base_path + ".vtt"
    ass_subtitle_path = base_path + ".ass"
    if os.path.isfile(subtitle_path):
        return FileResponse(open(subtitle_path, "rb"), content_type="text/vtt")
    elif os.path.isfile(ass_subtitle_path):
        vtt_data = convert_ass_to_vtt(ass_subtitle_path)
        return HttpResponse(vtt_data, content_type="text/vtt")
    else:
        return HttpResponse(f"Subtitle file not found:{video_path}", status=404)


## TODO
def get_vtt_subtitle():
    pass


## 获取可预览文件的预览。视频，音频，文本，pdf，诸如此类
def get_file_preview(request, path: str):
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


##  TODO 获取文件缩略图。如果缩略图不存在，则创建缩略图。
## 对图像来说，直接返回自身；对视频而言，会尝试创建。
## def get_file_thumb(request, path: str):
# path = os.path.join("/", path)
# if not os.path.isfile(path):
#     return HttpResponse("File not found at: <br>" + str(path))
# ext = extlib.get_ext_no_dot(path)

# # 根据文件类型，返回不同的响应
# match extlib.get_file_type(path):
#     case "video":
#         response = FileResponse(open(path, "rb"), content_type=f"video/{ext}")
#         response["Accept-Ranges"] = "bytes"
#         return response
#     case "image":
#         response = FileResponse(open(path, "rb"), content_type=f"image/{ext}")
#         response["Accept-Ranges"] = "bytes"
#         return response
#     case _:
#         return HttpResponse("Thumb not supported for this file type")

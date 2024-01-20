from django.http import HttpResponse
from django.shortcuts import render
import os
import json


def file_browser(request, path=""):
    path = os.path.join("/", path)  # 待遍历文件夹

    if os.path.isdir(path):
        raws = os.listdir(path)
        raws = sorted(raws, key=lambda x: x.lower())  # 对raws进行按名称从A-Z, a-z的排序

        name = os.path.basename(path)  # 所在目录的名称

        # path是路径。 根据path路径下的文件创建两个字符串数组，字符串分别为path路径下所有子路径/文件的绝对路径
        file_paths = [os.path.join(path, raw) for raw in raws if os.path.isfile(os.path.join(path, raw))]
        file_names = [os.path.basename(file) for file in file_paths]

        folder_paths = [os.path.join(path, raw) for raw in raws if os.path.isdir(os.path.join(path, raw))]
        folder_names = [os.path.basename(folder) for folder in folder_paths]


        # return HttpResponse(f"This is a Folder {path},<br> files: {files},<br> folders: {folders}")
        return render(
            request,
            "file_browser/file_browser.html",
            {
                "path": path,
                "name": name,
                "file_names": json.dumps(file_names),
                "file_paths": json.dumps(file_paths),
                "folder_names": json.dumps(folder_names),
                "folder_paths": json.dumps(folder_paths),

                "preview_image" : False,
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
                    "extname": os.path.splitext(path)[1],
                },
            )

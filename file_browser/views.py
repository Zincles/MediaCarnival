from django.http import HttpResponse
from django.shortcuts import render
import os
import json


def file_browser(request, path=""):
    path = os.path.join("/", path)  # 待遍历文件夹

    if os.path.isdir(path):
        raws = os.listdir(path)

        # 对raws进行按名称从A-Z, a-z的排序
        raws = sorted(raws, key=lambda x: x.lower())

        # path是路径。 根据path路径下的文件创建两个字符串数组，字符串分别为path路径下所有子路径/文件的绝对路径
        files = [os.path.join(path, raw) for raw in raws if os.path.isfile(os.path.join(path, raw))]
        folders = [os.path.join(path, raw) for raw in raws if os.path.isdir(os.path.join(path, raw))]

        # return HttpResponse(f"This is a Folder {path},<br> files: {files},<br> folders: {folders}")
        return render(
            request,
            "file_browser/file_browser.html",
            {
                "path": path,
                "name": os.path.basename(path),
                "file_names": json.dumps([os.path.basename(file) for file in files]),
                "file_paths": json.dumps(files),
                "folder_names": json.dumps([os.path.basename(folder) for folder in folders]),
                "folder_paths": json.dumps(folders),
            },
        )


    elif os.path.isfile(path):
        return HttpResponse("This is a file:" + str(path))
    else:
        return HttpResponse("This is not a file or folder:" + str(path))

from django.http import HttpResponse
from django.shortcuts import render
import os
import json


def file_browser(request, path=""):
    path = os.path.join("/", path)  # 待遍历文件夹

    if os.path.isdir(path):
        raws = os.listdir(path)
        files = [file for file in raws if os.path.isfile(os.path.join(path, file))]
        folders = [folder for folder in raws if os.path.isdir(os.path.join(path, folder))]

        path_files_folders_json = json.dumps([path, files, folders])
        print(folders)
        

        return render(
            request,
            "file_browser/file_browser.html",
            {
                "PATH": path,
                "FILES": files,
                "FOLDERS": folders,
                "PATH_FILES_FOLDERS_JSON":path_files_folders_json,
            },
        )
    else:
        return HttpResponse("This is a file:", path)

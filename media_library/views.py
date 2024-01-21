from django.http import Http404, HttpResponse, HttpResponseRedirect
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
    print(all_library)
    return render(
        request,
        "media_library/libraries.html",
        {"LIBRARIES": all_library},
    )


# def file_browser(request):
#     # 文件浏览器。
#     return render(request, "media_library/file_browser.html")


def library_inspector(request, library_id):
    # 访问具体的某个媒体库，查看里面的内容。在Jellyfin里，等价于“进入某个节目中”，大概
    # 每个MediaLibrary一定由剧集组成。例如， someanime_S01E01, someanime_S01E02 都属于一个MediaLibrary,都是MediaUnit.
    # MediaLibrary的属性 unit 即是 “剧集” 文件夹。
    try:
        library = MediaLibrary.objects.get(id=library_id)
        root_nodes = library.root_nodes.all()

        return render(
            request,
            "media_library/library_inspector.html",
            {
                "UNITS": set(library.unit.all()),
                "LIBRARY": library,
                "LIBRARY_ID ": library.id,
                "LIBRARY_NAME": library.library_name,
                "LIBRARY_TYPE": library.library_type,
                "LIBRARY_STRUCTURE": library.structure_type,
            },
        )

    except MediaLibrary.DoesNotExist:
        print("media_library::library_inspector::ERROR: 访问的媒体库不存在！")
        raise Http404("媒体库ID不存在!")

    except Exception as e:
        print("media_library::library_inspector::ERROR: 访问的媒体库不存在！")
        raise Http404("ERROR!")


# class MyAPIView(APIView):
#     def get(self, request):
#         # 在这里编写处理GET请求的逻辑
#         data = {'message': '这是来自服务器的数据！'}
#         return Response(data, status=status.HTTP_200_OK)

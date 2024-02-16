from django.contrib import admin
from django.http import Http404, HttpResponse, FileResponse
from django.urls import include, path
from django.shortcuts import redirect
from . import apis


urlpatterns = [
    # API
    path(route="api/get_folder", view=apis.api_get_folder, name="api_get_folder"),
    path(route="api/get_file_preview/<path:path>", view=apis.get_file_preview, name="api_get_file_preview"),
    path(route="api/get_media_libraries", view=apis.get_media_libraries, name="get_media_libraries"),
    path(route="api/get_media_library_by_id", view=apis.get_media_library_by_id, name="get_media_library_by_id"),
    path(route="", view=admin.site.urls),
]

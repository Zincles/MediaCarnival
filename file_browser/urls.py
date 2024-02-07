from django.urls import path
from . import views
from . import apis

app_name = "file_browser"

urlpatterns = [
    # path(route="", view=views.home, name="home"),
    # path(route="browser/", view=views.file_browser),
    # path(route="browser/<path:path>", view=views.file_browser, name="file_browser"),
    # API
    path(route="api/get_folder", view=apis.api_get_folder, name="api_get_folder"),
    path(route="api/get_file_preview/<path:path>", view=apis.get_file_preview, name="api_get_file_preview"),
    path(route="api/get_subtitle/<path:video_path>", view=apis.get_subtitle, name="api_get_subtitle"),
]

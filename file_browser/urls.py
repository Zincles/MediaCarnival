from django.urls import path
from . import views
from . import apis

app_name = "file_browser"

urlpatterns = [
    path(route="", view=views.file_browser, name="home"),
    path(route="browser/<path:path>", view=views.file_browser, name="file_browser"),
    path(route="api/get_folder/<path:path>", view=apis.api_get_folder, name="api_get_folder"),
    path(route="api/get_file_preview/<path:path>", view=apis.get_file_preview, name="api_get_file_preview"),
]


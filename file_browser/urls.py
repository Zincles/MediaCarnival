from django.urls import path
from . import views


app_name = "file_browser"

urlpatterns = [
    path(route="", view=views.file_browser, name="home"),
    path(route="<path:path>", view=views.file_browser, name="file_browser"),
]

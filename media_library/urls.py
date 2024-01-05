from django.urls import path
from . import views


app_name = "media_library"

urlpatterns = [
    path(route="", view=views.home, name="home"),
    path(route="libraries", view=views.libraries, name="libraries"),
    path(route="file_browser", view=views.file_browser, name="file_browser"),
    path(route="library_inspector/<int:library_id>/", view=views.library_inspector, name="library_inspector"),
]

from django.urls import path
from . import views
from . import apis


app_name = "media_library"

urlpatterns = [
    path(route="", view=views.home, name="home"),
    path(route="libraries", view=views.libraries, name="libraries"),
    # path(route="file_browser", view=views.file_browser, name="file_browser"),
    path(route="library_inspector/<int:library_id>/", view=views.library_inspector, name="library_inspector"),
    
    path(route="api/get_media_libraries", view=apis.get_media_libraries, name="get_media_libraries"),
    path(route="api/get_media_library_by_id", view=apis.get_media_library_by_id, name="get_media_library_by_id"),
    
    
]

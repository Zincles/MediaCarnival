from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.shortcuts import redirect
from django.http import FileResponse


# 默认空值将重定向到 welcome 应用
def redirect_view(request):
    return redirect("/welcome")


def favicon_view(request):
    path_to_icon = "static/cdn/ico/tv.ico"
    return FileResponse(open(path_to_icon, "rb"), content_type="image/x-icon")


urlpatterns = [
    path(route="", view=redirect_view),
    path(route="favicon.ico", view=favicon_view),
    path(route="admin/", view=admin.site.urls),
    path(route="core/", view=include("core.urls")),
    path(route="media_library/", view=include("media_library.urls")),
    path(route="file_browser/", view=include("file_browser.urls")),
    path(route="welcome/", view=include("welcome.urls")),
    path(route="server_config/", view=include("server_config.urls")),
    path(route="user_config/", view=include("user_config.urls")),
]

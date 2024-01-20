from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


# 默认空值将重定向到 welcome 应用
def redirect_view(request):
    return redirect("/welcome")


urlpatterns = [
    path(route="", view=redirect_view),
    path(route="admin/", view=admin.site.urls),
    path(route="core/", view=include("core.urls")),
    path(route="media_library/", view=include("media_library.urls")),
    path(route="file_browser/", view=include("file_browser.urls")),
    path(route="welcome/", view=include("welcome.urls")),
]

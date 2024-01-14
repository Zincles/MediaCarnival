"""
MediaCarnival 项目的 URL 配置。

`urlpatterns` 列表将 URL 路由到视图。更多信息请参阅：
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
示例：
函数视图
    1. 添加导入语句: from my_app import views
    2. 在 urlpatterns 中添加 URL: path('', views.home, name='home')
基于类的视图
    1. 添加导入语句: from other_app.views import Home
    2. 在 urlpatterns 中添加 URL: path('', Home.as_view(), name='home')
包含另一个 URL 配置
    1. 导入 include() 函数: from django.urls import include, path
    2. 在 urlpatterns 中添加 URL: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="core/", view=include("core.urls")),
    path(route="media_library/", view=include("media_library.urls")),
    path(route="image_viewer/", view=include("image_viewer.urls")),
    path(route="file_browser/", view=include("file_browser.urls")),
    
]

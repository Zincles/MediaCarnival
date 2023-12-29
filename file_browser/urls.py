from django.urls import path

from . import views


urlpatterns = [
    path(route="", view=views.index),
    # path(route="<path:file_path>", view=views.browser),
]



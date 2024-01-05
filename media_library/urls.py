from django.urls import path
from . import views

urlpatterns = [
    path(route="", view=views.home),
    path(route="libraries", view=views.libraries),
    # path(route="<path:file_path>", view=views.browser),
]

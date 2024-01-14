from django.urls import path
from . import views


app_name = "image_viewer"

urlpatterns = [
    path(route="", view=views.blank, name="blank"), # Blank
    path(route="<path:image_path>/", view=views.image_viewer, name="library_inspector"),
]

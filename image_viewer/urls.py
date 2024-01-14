from django.urls import path
from . import views


app_name = "image_viewer"

urlpatterns = [
    path(route="", view=views.home, name="home"),  # Blank
    path(route="<path:image_path>/", view=views.load_image, name="library_inspector"),
]

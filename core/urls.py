from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path(route="file/<path:path>/", view=views.file, name="file"),  

]

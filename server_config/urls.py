from django.urls import path
from . import views

app_name = "server_config"

urlpatterns = [
    path(route="", view=views.server_config, name="home"),
]

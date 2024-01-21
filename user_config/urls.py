from django.urls import path
from . import views

app_name = "user_config"

urlpatterns = [
    path(route="", view=views.user_config, name="home"),
]

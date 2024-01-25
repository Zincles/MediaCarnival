from django.urls import path
from . import views
from . import apis

app_name = "user_config"

urlpatterns = [
    path(route="", view=views.user_config, name="home"),
    path(route="api/get_user_config/", view=apis.get_user_config, name="api_get_user_config"),
]

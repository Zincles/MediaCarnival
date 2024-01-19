from django.urls import path
from . import views


app_name = "welcome"

urlpatterns = [
    path(route="", view=views.home, name="home"),
]

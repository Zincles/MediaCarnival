from django.shortcuts import render

# Create your views here.


def server_config(request):
    return render(
        request,
        "server_config/server_config.html",
        {},
    )

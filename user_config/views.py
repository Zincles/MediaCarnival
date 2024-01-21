from django.shortcuts import render


def user_config(request):
    return render(
        request,
        "user_config/user_config.html",
        {
            "username": request.user.username,
            "user_id": request.user.id,
        },
    )

import json
from django.forms import model_to_dict
from django.http import HttpResponse

from core.models import MediaLibrary


def get_media_libraries(request):
    libraries = [
        model_to_dict(
            lib,
            [
                "id",
                "library_name",
            ],
        )
        for lib in MediaLibrary.objects.all()
    ]
    return HttpResponse(
        json.dumps(
            {
                "libraries": libraries,
            }
        )
    )


def get_media_library_by_id(request):
    library_id = request.GET.get("library_id")
    return HttpResponse(f"OK, id is {library_id}")
    return MediaLibrary.objects.get_or_create(site_id=1)[0]

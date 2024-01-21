from django.contrib import admin
from .models import TmdbAccessToken


class TmdbAccessTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "value")
    list_display_links = ("id", "value")


admin.site.register(TmdbAccessToken, TmdbAccessTokenAdmin)

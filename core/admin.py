from django.contrib import admin
from core.models import FSNode


class FSNodeAdmin(admin.ModelAdmin):
    list_display = ["id", "parent", "path"]
    list_filter = ["parent"]
    search_fields = ["path"]


admin.site.register(FSNode, FSNodeAdmin)
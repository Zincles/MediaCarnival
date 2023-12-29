from django.contrib import admin
from core.models import FSNode


class FSNodeAdmin(admin.ModelAdmin):
    list_display = ["id", "parent", "absolute_path"]
    list_filter = ["parent"]
    search_fields = ["absolute_path"]


admin.site.register(FSNode, FSNodeAdmin)
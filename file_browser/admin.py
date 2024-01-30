from django.contrib import admin
from .models import Thumbnail
# Register your models here.

## ThumbnailAdmin
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ("path", "thumbnail", "file_created_at", "file_updated_at", "created_at", "updated_at")
    list_filter = ("file_created_at", "file_updated_at", "created_at", "updated_at")
    search_fields = ("path", "thumbnail", "file_created_at", "file_updated_at", "created_at", "updated_at")
    date_hierarchy = "created_at"


    # 覆写管理员面板的删除方法，使其能够删除缩略图文件。
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()



admin.site.register(Thumbnail, ThumbnailAdmin)
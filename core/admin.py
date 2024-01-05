from django.contrib import admin
from core.models import FSNode, MediaLibrary, MediaUnit
from django.contrib import admin


# 文件节点
class FSNodeAdmin(admin.ModelAdmin):
    list_display = [
        "_get_basename",
        "_get_filetype",
        "id",
        "path",
        "parent",
    ]
    #    list_filter = ["parent"]
    search_fields = ["path"]

    @admin.display(description="文件名")
    def _get_basename(self, node):
        return node.get_path_basename()

    @admin.display(description="类型")
    def _get_filetype(self, node) -> str:
        if node.is_directory():
            return "目录"
        else:
            return "文件"

    @admin.action(description="对该节点进行递归更新。")
    def update_recursively(modeladmin, request, queryset):
        for i in queryset:
            i.update_recursively()
        # queryset.update(status="p")

    actions = [update_recursively]


# 库节点
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ["library_name", "id", "_get_root_node_nums", "library_type", "structure_type"]
    filter_horizontal = ("root_nodes",)

    @admin.display(description="根路径数量")
    def _get_root_node_nums(self, library):
        nodes = library.root_nodes.all()
        num = len(nodes)
        return str(num)

    @admin.action(description="扫描库")
    def scan_library(modeladmin, request, queryset):
        for i in queryset:
            i.scan_library()
    actions = [scan_library]


class MediaUnitAdmin(admin.ModelAdmin):
    list_display = ["library", "fsnode", "nickname"]


admin.site.register(MediaLibrary, MediaLibraryAdmin)
admin.site.register(FSNode, FSNodeAdmin)
admin.site.register(MediaUnit, MediaUnitAdmin)
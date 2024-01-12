from django.contrib import admin
from core.models import FSNode, MediaLibrary, MediaUnit
from core.models import TmdbTvSeriesDetails, TmdbTvSeasonDetails, TmdbTvEpisodeDetails, TmdbMovieDetails
from django.contrib import admin

from django.utils import timezone
from datetime import datetime, timedelta

from debug_settings import ACCESS_TOKEN


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


# 媒体单元
class MediaUnitAdmin(admin.ModelAdmin):
    list_display = ["library", "fsnode", "nickname"]
    filter_horizontal = ("metadata_tmdb_tv", "metadata_tmdb_movie")


# TMDB Series
class TmdbTvSeriesDetailsAdmin(admin.ModelAdmin):
    @admin.action(description="单独更新节点的元数据（300s）")
    def update(modeladmin, request, queryset):
        for i in queryset:
            i.update(ACCESS_TOKEN, 300)

    @admin.action(description="深度更新节点的元数据（300s）")
    def deep_update(modeladmin, request, queryset):
        for i in queryset:
            i.deep_update(AUTH=ACCESS_TOKEN, tolerate_time=300)

    actions = ["update", "deep_update"]

    list_display = ["series_id", "updated_time", "get_name", "get_update_timedelta"]
    truncatewords = 10
    # truncatechars:10


# TMDB Season
class TmdbTvSeasonDetailsAdmin(admin.ModelAdmin):
    @admin.action(description="单独更新节点的元数据（300s）")
    def update(modeladmin, request, queryset):
        for i in queryset:
            i.update(ACCESS_TOKEN, 300)

    @admin.display(description="获取Metadata的预览")
    def _get_meta_preview(self, meta):
        r = str(meta.metadata)
        result = r[:30] + "   ......   " + r[-30:]
        return result

    actions = ["update"]
    list_display = ["series_id", "season_number", "updated_time", "_get_meta_preview", "get_update_timedelta"]


# TMDB Episode
class TmdbTvEpisodeDetailsAdmin(admin.ModelAdmin):
    @admin.action(description="单独更新节点的元数据（300s）")
    def update(modeladmin, request, queryset):
        for i in queryset:
            i.update(ACCESS_TOKEN, 300)

    @admin.display(description="获取Metadata的预览")
    def _get_meta_preview(self, meta):
        r = str(meta.metadata)
        result = r[:30] + "   ......   " + r[-30:]
        return result

    actions = ["update"]
    list_display = [
        "series_id",
        "season_number",
        "episode_number",
        "updated_time",
        "_get_meta_preview",
        "get_update_timedelta",
    ]


class TmdbMovieDetailsAdmin(admin.ModelAdmin):
    @admin.display(description="获取Metadata的预览")
    def _get_meta_preview(self, meta):
        r = str(meta.metadata)
        result = r[:30] + "   ......   " + r[-30:]
        return result

    list_display = ["movie_id", "_get_meta_preview"]


admin.site.register(MediaLibrary, MediaLibraryAdmin)
admin.site.register(FSNode, FSNodeAdmin)
admin.site.register(MediaUnit, MediaUnitAdmin)

admin.site.register(TmdbTvSeriesDetails, TmdbTvSeriesDetailsAdmin)
admin.site.register(TmdbTvSeasonDetails, TmdbTvSeasonDetailsAdmin)
admin.site.register(TmdbTvEpisodeDetails, TmdbTvEpisodeDetailsAdmin)
admin.site.register(TmdbMovieDetails, TmdbMovieDetailsAdmin)

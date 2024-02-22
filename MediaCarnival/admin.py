#   ALL CODE WRITTEN BY Down Zincles, Following GPLv3 Lisence.
from django.contrib import admin, messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .lib import strlib


# 获取TMDB Access Token
def get_tmdb_access_token():
    return TmdbAccessToken.objects.first().value


# 文件节点
class FSNodeAdmin(admin.ModelAdmin):
    list_display = ["_get_basename", "is_accessible", "_get_filetype", "id", "path", "parent_id"]
    list_display_links = [
        "_get_basename",
        "id",
        "path",
    ]
    list_filter = ["parent"]
    search_fields = ["path"]

    @admin.display(description="文件名")
    def _get_basename(self, node):
        return node.get_basename()

    @admin.display(description="类型")
    def _get_filetype(self, node) -> str:
        if node.is_directory():
            return "目录"
        else:
            return "文件"

    @admin.action(description="对该节点进行递归更新。")
    def update_recursively(modeladmin, request, queryset):
        for i in queryset:
            try:
                i.update_recursively()
                messages.success(request, f"已对节点 {i} 进行递归更新。")
            except Exception as e:
                messages.error(request, f"节点 {i} 更新失败。原因：{e}")

    @admin.action(description="删除无效节点")
    def delete_invalid_nodes(modeladmin, request, queryset):
        for i in queryset:
            i.delete_if_unaccessible()

    actions = [update_recursively, delete_invalid_nodes]


# 库节点
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ["library_name", "id", "_get_root_node_nums", "library_type", "structure_type"]
    filter_horizontal = ("root_nodes",)

    @admin.display(description="根路径数量")
    def _get_root_node_nums(self, library):
        nodes = library.root_nodes.all()
        num = len(nodes)
        return str(num)

    @admin.action(description="重新扫描所有库")
    def rescan_library(modeladmin, request, queryset):
        for i in queryset:
            try:
                i.rescan_library()
                messages.success(request, f"已对库 {i} 进行扫描。")
            except Exception as e:
                messages.error(request, f"库 {i} 扫描失败。原因：{e}")

    @admin.action(description="更新所有根节点，然后重新扫描")
    def update_nodes_then_rescan_library(modeladmin, request, queryset):
        for i in queryset:
            try:
                i.update_root_nodes()
                messages.success(request, f"已对库 {i} 进行根节点更新。")

                i.rescan_library()
                messages.success(request, f"已对库 {i} 进行扫描。")

            except Exception as e:
                messages.error(request, f"库 {i} 根节点更新失败。原因：{e}")
            finally:
                pass

    actions = [rescan_library, update_nodes_then_rescan_library]


# 媒体单元
class MediaUnitAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_basename",
        "unit_type",
        "tmdb_id",
        "library",
        "fsnode",
        "nickname",
        "_get_tmdb_metadata_status",
    ]
    list_display_links = ["get_basename", "fsnode"]
    filter_horizontal = ("metadata_tmdb_tv", "metadata_tmdb_movie")

    @admin.display(description="TMDB元数据状况")
    def _get_tmdb_metadata_status(self, unit):
        if unit.metadata_tmdb_tv.exists() or unit.metadata_tmdb_movie.exists():
            return "已获取"
        else:
            return "未获取"

    @admin.action(description="根据文件夹名称，查询TMDB ID")
    def _update_tmdb_id_by_basename(modeladmin, request, queryset):
        for i in queryset:
            try:
                i.update_tmdb_id_by_folder_name(get_tmdb_access_token())
                messages.success(request, f"已对Unit {i} 更新了ID: {i.tmdb_id}。")
            except Exception as e:
                messages.error(request, f"节点 {i} 更新ID失败。原因：{e}")

    @admin.action(description="根据已有ID和类型，获取Series元数据并附加")
    def _update_tmdb_metadata_by_id(modeladmin, request, queryset):
        for i in queryset:
            try:
                i.update_tmdb_metadata_by_id(get_tmdb_access_token())
                messages.success(request, f"已对Unit {i} 更新了元数据。")
            except Exception as e:
                messages.error(request, f"节点 {i} 更新元数据失败。原因：{e}")

    @admin.action(description="显示已有的媒体文件数组")
    def _show_media_files(modeladmin, request, queryset):
        for i in queryset:
            try:
                F = [fnode.get_basename() for fnode in i.get_media_files()]

                messages.info(request, f"Unit {i} 的媒体文件：{F}")
            except Exception as e:
                messages.error(request, f"节点 {i} 获取媒体文件失败。原因：{e}")

    @admin.action(description="根据已有TMDB ID，获取元数据并附加")
    def _attach_tmdb_metadata_by_id(modeladmin, request, queryset):
        for i in queryset:
            try:
                i.attach_tmdb_metadata_by_id(get_tmdb_access_token())
                messages.success(request, f"已对Unit {i} 附加了元数据。")
            except Exception as e:
                messages.error(request, f"节点 {i} 附加元数据失败。原因：{e}")

    actions = [_update_tmdb_id_by_basename, _show_media_files, _attach_tmdb_metadata_by_id]


# TMDB Series
class TmdbTvSeriesDetailsAdmin(admin.ModelAdmin):
    @admin.action(description="单独更新节点的元数据（300s）")
    def update(modeladmin, request, queryset):
        for i in queryset:
            i.update(get_tmdb_access_token(), 300)

    @admin.action(description="深度更新节点的元数据（300s）")
    def deep_update(modeladmin, request, queryset):
        for i in queryset:
            i.deep_update(AUTH=get_tmdb_access_token(), tolerate_time=300)

    actions = ["update", "deep_update"]

    list_display = ["series_id", "updated_time", "get_name", "get_update_timedelta"]
    truncatewords = 10


# TMDB Season
class TmdbTvSeasonDetailsAdmin(admin.ModelAdmin):
    @admin.action(description="单独更新节点的元数据（300s）")
    def update(modeladmin, request, queryset):
        for i in queryset:
            i.update(get_tmdb_access_token(), 300)

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
            i.update(get_tmdb_access_token(), 300)

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


# TMDB Movie
class TmdbMovieDetailsAdmin(admin.ModelAdmin):
    @admin.display(description="获取Metadata的预览")
    def _get_meta_preview(self, meta):
        r = str(meta.metadata)
        result = r[:30] + "   ......   " + r[-30:]
        return result

    list_display = ["movie_id", "_get_meta_preview"]


## 管理缩略图
class ThumbnailAdmin(admin.ModelAdmin):
    list_display = ("path", "thumbnail", "file_created_at", "file_updated_at", "created_at", "updated_at")
    list_filter = ("file_created_at", "file_updated_at", "created_at", "updated_at")
    search_fields = ("path", "thumbnail", "file_created_at", "file_updated_at", "created_at", "updated_at")
    date_hierarchy = "created_at"

    # 覆写管理员面板的删除方法，使其能够删除缩略图文件。
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


# 管理TMDB Access Token
class TmdbAccessTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "value")
    list_display_links = ("id", "value")


# 管理用户配置
class UserConfigAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "language"]
    list_display_links = ["id", "user"]

    def __str__(self) -> str:
        return f"[UserConfig: {self.user.username}]"


admin.site.register(MediaLibrary, MediaLibraryAdmin)
admin.site.register(FSNode, FSNodeAdmin)
admin.site.register(MediaUnit, MediaUnitAdmin)
admin.site.register(TmdbTvSeriesDetails, TmdbTvSeriesDetailsAdmin)
admin.site.register(TmdbTvSeasonDetails, TmdbTvSeasonDetailsAdmin)
admin.site.register(TmdbTvEpisodeDetails, TmdbTvEpisodeDetailsAdmin)
admin.site.register(TmdbMovieDetails, TmdbMovieDetailsAdmin)
admin.site.register(Thumbnail, ThumbnailAdmin)
admin.site.register(TmdbAccessToken, TmdbAccessTokenAdmin)
admin.site.register(UserConfig, UserConfigAdmin)

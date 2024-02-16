#   ALL CODE WRITTEN BY Down Zincles, Following GPLv3 Lisence.
from requests import Response
from .lib import hash, tmdb_api
from django.utils import timezone
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from datetime import datetime, timedelta
from moviepy.editor import VideoFileClip
import os, tempfile


class MediaLibrary(models.Model):
    """
    这是媒体库的基类. 一个媒体库中可保存多个MediaUnit.
    根据MediaLibrary类型的不同,可以生成不同的MediaUnit.
    """

    library_name = models.CharField(max_length=128, null=False)  # 媒体库的，显示在用户面前的名称
    root_nodes = models.ManyToManyField("FSNode")  # 媒体库的根节点们

    # 可能的类型： TV FILMS IMAGES MUSICS BOOKS FILES
    library_type = models.CharField(max_length=128, null=False, default="TV")

    # "COMPLEX(自定义指定)", "FLAT(一个文件夹对应一个Series)"
    structure_type = models.CharField(max_length=128, null=False, default="FLAT")

    class Meta:
        verbose_name = "媒体库"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "[媒体库：" + self.library_name + "]"

    def create_library(path, library_type="SHOWS", structure_type="FLAT"):
        """创建库."""
        node = path if path is FSNode else FSNode(path=path)  # Path可以输入为节点/字符串.
        return MediaLibrary(root_node=node, library_type=library_type, structure_type=structure_type)

    def update_root_nodes(self):
        """对每个根节点执行递归扫描"""
        for node in self.root_nodes.all():
            node.update_recursively()

    def rescan_library(self, scan_type="FLAT"):
        """重扫描库。通过FSNode与文件系统通信。"""
        try:
            for unit in self.unit.all():  # 清除现有的Units
                unit.delete()
            match scan_type:  # 根据预设进行行动
                case "FLAT":  # 标注模式
                    for root_node in self.root_nodes.all():  # 遍历根节点们
                        # 获取所有文件节点(非目录)。平放到一个数组里。
                        folder_nodes = {node for node in root_node.get_children() if node.is_directory()}

                        # 为每个文件夹创建MediaUnit.
                        for node in folder_nodes:
                            unit = MediaUnit(library=self, fsnode=node)
                            unit.save()
                case _:
                    raise Exception("指定了错误的媒体库扫描类型！")
        except Exception as e:
            print("扫描库中遇到错误：", e)
            raise e


class MediaUnit(models.Model):
    """
    媒体单位。只能由MediaLibrary创建。单位是“SERIES / MOVIE”
    必须指定Library, 且必须由Library创建。必须指向一个FSNode。
    """

    library = models.ForeignKey(to="MediaLibrary", on_delete=models.CASCADE, null=False, related_name="unit")
    fsnode = models.ForeignKey(to="FSNode", on_delete=models.CASCADE, null=False)

    tmdb_id = models.IntegerField(null=True, blank=True)  # tmdb ID
    unit_type = models.CharField(max_length=64, null=False, default="TV")
    # "TV" "FILMS" "IMAGES" "MUSICS" "BOOKS" "FILES"

    nickname = models.CharField(max_length=512, null=True, blank=True)  # 自定义别名. 由用户手动指定

    # TV剧集元数据。一个媒体Unit在创建时，必须指定其指向的位置，与类型。
    metadata_tmdb_tv = models.ManyToManyField(to="TmdbTvSeriesDetails", related_name="media_unit", blank=True)
    metadata_tmdb_movie = models.ManyToManyField(to="TmdbMovieDetails", related_name="media_unit", blank=True)

    class Meta:
        verbose_name = "媒体单位"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return "[MediaUnit: " + self.fsnode.path + "]"

    def get_basename(self):
        "获取文件夹名称."
        return os.path.basename(self.fsnode.get_basename())

    def update_tmdb_id_by_folder_name(self, AUTH):
        """根据文件夹名称,查询并更新tmdb_id。需要API key. 遇到错误则抛出。"""
        try:
            match self.unit_type:
                case "TV":
                    id = tmdb_api.get_tv_id_by_name(AUTH, self.get_basename())
                    self.tmdb_id = id
                    self.save()
                    print(f"类型为TV, 文件夹名为{self.get_basename()}, ID为{id}")

                case "MOVIE":
                    id = tmdb_api.get_movie_id_by_name(AUTH, self.get_basename())
                    self.tmdb_id = id
                    self.save()
                    print(f"类型为MOVIE, 文件夹名为{self.get_basename()}, ID为{id}")

                case _:
                    raise Exception(f"错误的媒体类型！: {self.unit_type}不受支持！")

        except Exception as e:
            print("更新tmdb_id时遇到错误:", e)
            raise e


# ============================== #
#                                #
#        TMDB 的 基础元数据        #
#                                #
# ============================== #


class TmdbAccessToken(models.Model):
    """TheMovieDB的访问令牌"""

    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.value[:25] + "..."

    def get_first_value() -> str:
        return TmdbAccessToken.objects.first().value


class TmdbTvSeriesDetails(models.Model):
    """TMDB 剧集系列元数据信息"""

    series_id = models.IntegerField(null=False)  # 剧集ID, 必须有数值

    updated_time = models.DateTimeField(null=False)  # 本地的数据的更新时间
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "TMDB TV 系列 元数据"
        verbose_name_plural = verbose_name

    # TEST
    def get_or_create_or_update(self, AUTH, tolerate_time=0):
        """获取或创建或更新一个Series的元数据。"""
        series_id = self.series_id
        try:
            existed = TmdbTvSeriesDetails.objects.get(series_id=series_id)
            existed.update(AUTH, tolerate_time)  # 尝试更新
            return existed
        except TmdbTvSeriesDetails.DoesNotExist:  # 本地没有元数据，创建之
            new = TmdbTvSeriesDetails(series_id=series_id)
            new.save()
            new.update(AUTH, tolerate_time)
            return new
        except Exception as e:
            print("get_or_create_or_update()::遇到错误:", e)
            return

    ## 获取更新时间距今的时间差。
    def get_update_timedelta(self):
        updated_time: datetime = self.updated_time
        current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)
        td: timedelta = current_time - updated_time
        return td

    ## 仅尝试更新Series本身的元数据。不会对子资源进行操作。
    def update(self, AUTH, tolerate_time=0):
        try:
            # 判断是否在容忍范围内。如果在，则忽略本次更新。
            updated_time: datetime = self.updated_time
            current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)
            td: timedelta = current_time - updated_time
            if tolerate_time > 0 and td.total_seconds() < tolerate_time:  # 如果有设置容忍时间且时间差在容忍范围内
                print("在容忍范围内，无需更新!")
                return

            response = tmdb_api.request_tv_series_detail(AUTH, self.series_id)

            # 如果遭遇错误，则抛出错误并结束; 如果正常，则将获得字典存入。
            if response.status_code != 200:
                raise Exception("tmdb_api.request_tv_series_detail()::返回结果不为200!")
            else:
                self.updated_time = current_time  # 更新时间
                self.metadata = response.json()  # 写入字典
                self.save()  # 保存

        except Exception as e:
            print("更新系列元数据遇到异常", e)

    ## 深度更新。
    ## create_meta 代表是否为库内没有节点的剧集创建节点？ update_seasons/episodes代表是否更新相关的剧集/节目，
    ## tolerate_time_s 代表容忍时间，假设元数据足够新（据现在时间小于Tolerate,则不更新直接跳过。当然，不会跳过它的子节点）
    def deep_update(self, AUTH, create_meta=True, update_seasons=True, update_episodes=True, tolerate_time=0):
        try:
            updated_time: datetime = self.updated_time
            current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)

            if create_meta == True:
                print("允许创建元数据节点")

            # 更新自己
            self.update(AUTH, tolerate_time)

            # 获得已存在的Season节点。
            existed_season_metas = set(TmdbTvSeasonDetails.objects.filter(series_id=self.series_id))
            existed_season_meta_nums: set[int] = {i.season_number for i in existed_season_metas}  # 已有的剧集的ID

            print("Existed Metas: ", existed_season_metas)

            # 更新已有的Season节点
            for season_meta in existed_season_metas:
                print("\t尝试更新已有的Season节点...")
                season_meta.update(AUTH, tolerate_time)

            # 更新没有有的Season节点。(会创建节点)
            if create_meta:
                for season_dict in self.metadata["seasons"]:
                    season_num = int(season_dict["season_number"])  # 每个剧集的剧集ID

                    if not season_num in existed_season_meta_nums:
                        # 如果找到了缺失元数据的季，则创建节点并添加之，然后更新。
                        season_meta = TmdbTvSeasonDetails(
                            series_id=self.series_id, season_number=season_num, updated_time=current_time
                        )
                        season_meta.save()
                        season_meta.update(AUTH, tolerate_time=0)
                        print("创建了Season元数据节点并进行初始化更新了")

            # 更新节目 Episode相关的数据. 找到所有季 Season， 然后遍历
            print("寻找所有已有季, 以开始遍历Episode")
            existed_season_metalist = set(TmdbTvSeasonDetails.objects.filter(series_id=self.series_id))

            for season_meta in existed_season_metalist:
                season_num = season_meta.season_number
                print(f"正在遍历第 {season_num} 季")

                # 找到这个季里的所有已存在Episode (节目=当前节目， 季号=当前季)
                existed_episodes = set(
                    TmdbTvEpisodeDetails.objects.filter(series_id=self.series_id, season_number=season_num)
                )
                existed_episode_meta_nums: set[int] = {i.episode_number for i in existed_episodes}  # 已有的节目的ID

                print(f"找到了已有Episodes:{existed_episodes}")

                # 遍历每个已存在Episode, 并进行更新
                for episode in existed_episodes:
                    episode.update(AUTH, tolerate_time)

                # 对于不存在节点的，根据参数选择是否创建节点并更新
                if create_meta:
                    for episode_dict in season_meta.metadata["episodes"]:
                        season_num = int(episode_dict["season_number"])  # 每个剧集的剧集ID
                        episode_num = int(episode_dict["episode_number"])

                        if not episode_num in existed_episode_meta_nums:
                            # 如果找到了缺失元数据的季，则创建节点并添加之，然后更新。
                            episode_meta = TmdbTvEpisodeDetails(
                                series_id=self.series_id,
                                season_number=season_num,
                                episode_number=episode_num,
                                updated_time=current_time,
                            )
                            episode_meta.save()
                            episode_meta.update(AUTH, tolerate_time=0)
                            print("\t\t创建了Episode元数据节点并进行初始化更新了")

        except Exception as e:
            print("deep_update遇到错误:", e)
            pass

    def get_name(self):
        """获取该节目的名称（本地名称）"""
        try:
            name = self.metadata["name"]
            return name
        except Exception as e:
            print(f"错误： {e}")
            return f"ERROR!{e}"

    def __str__(self) -> str:
        try:
            name: str = self.metadata["name"] if not self.metadata is None else "N/A"
            return f"[TMDB Series: ID={self.series_id} NAME={name}]"
        except Exception as e:
            print(f"错误：{e}")
            return f"[TMDB Series ERROR! 获取名称失败,{e}]"


class TmdbTvSeasonDetails(models.Model):
    """TMDB剧集的 Season 信息"""

    series_id = models.IntegerField(null=False)
    season_number = models.IntegerField(null=False)

    updated_time = models.DateTimeField()  # 本地的数据的更新时间
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "TMDB TV 季 元数据"
        verbose_name_plural = verbose_name

    ## 获取更新时间距今的时间差。
    def get_update_timedelta(self):
        updated_time: datetime = self.updated_time
        current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)
        td: timedelta = current_time - updated_time
        return td

    def update(self, AUTH, tolerate_time=0):
        """尝试更新Season的元数据。与Series基本一致"""
        try:
            updated_time: datetime = self.updated_time
            current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)
            td: timedelta = current_time - updated_time
            if tolerate_time > 0 and td.total_seconds() < tolerate_time:  # 如果有设置容忍时间且时间差在容忍范围内
                print("在容忍范围内，无需更新!")
                return

            response = tmdb_api.request_tv_season_detail(AUTH, self.series_id, self.season_number)

            if response.status_code != 200:
                raise Exception("tmdb_api.request_tv_season_detail()::返回结果不为200!")
            else:
                self.updated_time = current_time  # 更新时间
                self.metadata = response.json()  # 写入字典
                self.save()  # 保存

        except Exception as e:
            print("更新Season元数据遇到异常", e)


class TmdbTvEpisodeDetails(models.Model):
    """TMDB具体Episode的信息"""

    series_id = models.IntegerField(null=False)
    season_number = models.IntegerField(null=False)
    episode_number = models.IntegerField(null=False)

    updated_time = models.DateTimeField()  # 本地的数据的更新时间
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "TMDB TV 剧集 元数据"
        verbose_name_plural = verbose_name

    ## 获取更新时间距今的时间差。
    def get_update_timedelta(self):
        updated_time: datetime = self.updated_time
        current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)
        td: timedelta = current_time - updated_time
        return td

    def update(self, AUTH, tolerate_time=0):
        """尝试更新Episode的元数据。与Series基本一致"""
        try:
            updated_time: datetime = self.updated_time
            current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)
            td: timedelta = current_time - updated_time
            if tolerate_time > 0 and td.total_seconds() < tolerate_time:  # 如果有设置容忍时间且时间差在容忍范围内
                print("在容忍范围内，无需更新!")
                return

            response = tmdb_api.request_tv_episode_detail(AUTH, self.series_id, self.season_number, self.episode_number)

            if response.status_code != 200:
                raise Exception("tmdb_api.request_tv_episode_detail()::返回结果不为200!")
            else:
                self.updated_time = current_time  # 更新时间
                self.metadata = response.json()  # 写入字典
                self.save()  # 保存

        except Exception as e:
            print("更新Episode元数据遇到异常", e)


class TmdbMovieDetails(models.Model):
    """电影的元数据"""

    movie_id = models.IntegerField(null=False)
    updated_time = models.DateTimeField(null=False)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "TMDB Movie 元数据"
        verbose_name_plural = verbose_name

    ## 更新元数据。与TV Series的方法相同
    def update(self, AUTH, tolerate_time=0):
        try:
            updated_time: datetime = self.updated_time
            current_time: datetime = datetime.now().astimezone(updated_time.tzinfo)
            td: timedelta = current_time - updated_time
            if tolerate_time > 0 and td.total_seconds() < tolerate_time:  # 如果有设置容忍时间且时间差在容忍范围内
                print("在容忍范围内，无需更新!")
                return

            response = tmdb_api.request_movie_detail(AUTH, self.movie_id)

            # 如果遭遇错误，则抛出错误并结束; 如果正常，则将获得字典存入。
            if response.status_code != 200:
                raise Exception("tmdb_api.request_movie_detail()::返回结果不为200!")
            else:
                self.updated_time = current_time  # 更新时间
                self.metadata = response.json()  # 写入字典
                self.save()  # 保存

        except Exception as e:
            print("更新系列元数据遇到异常", e)


# ================================ #
#                                  #
#         TMDB 的 图像元数据         #
#                                  #
# ================================ #


class TmdbImageFile(models.Model):
    """从TMDB抓取的图像缓存。"""

    @staticmethod
    def save_image(image_path: str):
        pass

    @staticmethod
    def get_image(image_path: str):
        pass

    class Meta:
        verbose_name = "TMDB图像文件"
        verbose_name_plural = verbose_name


# =================================== #
#                                     #
#            文件系统的中间层            #
#                                     #
# =================================== #


# 文件系统的节点树.
class FSNode(models.Model):
    """
    文件系统的映射节点. 用于供媒体库使用.映射树内的每个节点,对应着真实路径下的某个位置.
    节点的属性并非实时更新的. 需要使用函数手动递归更新.
    """

    HASH_METHOD = "md5"  # 默认的哈希方法

    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, null=True, blank=True, related_name="child")
    path = models.CharField(max_length=512)  # 所指向的绝对路径

    # 文件元数据. 非实时, 需手动更新.
    meta_size = models.BigIntegerField(null=True, blank=True)
    meta_hash = models.CharField(max_length=512, null=True, blank=True)
    meta_last_modified_time = models.DateTimeField(null=True, blank=True, auto_now=True)
    meta_last_created_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = "文件节点"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.path)

    def get_basename(self) -> str:
        """获取路径的文件的basename.例如, /home/user/sth.txt -> sth.txt."""
        return os.path.basename(self.path)

    def is_directory(self) -> bool:
        return os.path.isdir(self.path)

    def is_file(self) -> bool:
        return os.path.isfile(self.path)

    def is_accessible(self) -> bool:
        return os.access(self.path, os.R_OK)

    def get_child(self, child_name: str):
        """根据名称获取单层子节点"""
        for child in self.child.all():
            if child_name == os.path.basename(child.path):
                return child
        raise Exception("core::FSNode::get_child(): 错误!未能找到Child! 输入文件名为: " + child_name)

    def get_children(self, deep=False):
        """获取当前节点的所有子节点. 如果deep=True,则返回所有子节点的子节点."""
        if deep == False:
            return set(self.child.all())
        else:
            if not os.path.isdir(self.path):  # 返回当前节点的所有子节点的get_children()的并集
                return set([])
            result = set(self.child.all())

            for child_node in result:  # 遍历当前子节点:
                result = result.union(child_node.get_children(deep=True))
            return result

    def get_parent_id(self):
        """获取父节点的ID. 如果没有父节点,则返回None. TEST"""
        return self.parent.id if not self.parent is None else None

    def get_untracked_basenames(self):
        """获取未被追踪的文件的名称(basename)"""
        children_names = {os.path.basename(i.path) for i in self.get_children()}
        filenames_in_path = set(os.listdir(self.path))
        untracked = filenames_in_path - children_names
        return untracked

    def get_lost_track_nodes(self):
        """获取丢失跟踪的子节点"""
        children_names = {os.path.basename(i.path) for i in self.get_children()}
        filenames_in_path = set(os.listdir(self.path))
        lost_track = children_names - filenames_in_path
        return {self.get_child(i) for i in lost_track}

    def delete_if_unaccessible(self):
        """如果自己不可访问,则删除自己 TEST"""
        if not self.is_accessible():
            self.delete()

    def delete_all_children(self):
        """删除所有子节点 TEST"""
        for child in self.get_children():
            child.delete()

    def delete_unaccessible_children(self):
        """删除不可访问的子节点 TEST"""
        for child in self.get_children():
            if not child.is_accessible():
                child.delete()

    def update_hash(self):
        """更新文件的哈希值"""
        self.meta_hash = hash.get_file_hash(self.path, method=self.HASH_METHOD)

    def update_recursively(self, ttl: int = 10) -> None:
        """递归更新文件映射树."""
        if ttl <= 0:  # 确保自己没有抵达最大深度
            raise Exception("抵达最大深度")
        if not os.path.isdir(self.path):  # 确保自己是目录.
            raise Exception("节点不可以被遍历")
        if not self.is_accessible():  # 确保自己是可访问的.
            raise Exception("节点不可访问")

        try:
            for untracked_basename in self.get_untracked_basenames():  # 为未追踪的路径创建节点
                node = FSNode(path=os.path.join(self.path, untracked_basename), parent=self)
                node.save()

            lost_track_nodes = self.get_lost_track_nodes()  # 移除丢失追踪的节点
            for n in lost_track_nodes:
                n.delete()

            self.save()  # 保存自己

            try:  # 尝试对自己的children迭代call.
                for child_node in self.get_children():
                    child_node.update_recursively(ttl - 1)
            except Exception as e:
                print("迭代遇到错误:", e)

            self.save()  # 再次尝试保存
            print(f"[info]节点更新完毕: {self.path}")

        except Exception as e:
            print("异常发生(core::update_recursively):\n\t", e)
            return

    def update_metadata(self):
        """更新当前节点的元数据. TEST this"""
        try:
            abs_path = self.path
            if os.path.isdir(abs_path):
                """是目录"""
                print("是目录.")

            else:
                """是文件"""
                print("是文件.计算.")
                self.meta_size = os.path.getsize(abs_path)
                self.meta_hash = hash.get_file_hash(file_abs_path=self.path)

                self.meta_last_modified_time = os.path.getmtime(self.path)
                self.meta_last_created_time = os.path.getctime(self.path)

        except Exception as e:
            print(f"更新元数据时遇到错误:{e}")


# ================================ #
#                                  #
#            用户设置相关            #
#                                  #
# ================================ #


class UserConfig(models.Model):
    """用户配置"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_config")

    # 用户状态
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # 个人设置
    language = models.CharField(max_length=255, null=True, blank=True, default="zh-CN")
    file_browser_cols = models.IntegerField(null=False, blank=False, default=4)

    # 个人收藏的目录位置信息
    favorite_paths = models.JSONField(default=dict)

    ## 设置个人收藏的目录位置信息
    def set_favorate_path(self, name: str, path: str):
        path = os.path.abspath(path)

        # 读取favorite_paths作为字典, 写入键值对
        favorite_paths: dict = self.favorite_paths
        favorite_paths[name] = path

        # 保存
        self.favorite_paths = favorite_paths
        self.favorite_paths.save()

    ## 获取个人的所有收藏目录
    def get_favorate_paths(self, name: str):
        return self.favorite_paths[name]


# ================================ #
#                                  #
#            FileBrowser            #
#                                  #
# ================================ #


## 缩略图模型。通过创建时间与更新时间来判断是否需要更新。
class Thumbnail(models.Model):
    path = models.CharField(max_length=200, unique=True, blank=False, null=False)  # 原文件的文件系统中的路径
    thumbnail = models.ImageField(upload_to="thumbnails", blank=True, null=True)  # 缩略图

    # 文件的创建时间与更新时间。
    file_created_at = models.DateTimeField(blank=False, null=False)
    file_updated_at = models.DateTimeField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 可容忍的缩略图缓存时间。如果文件不存在了，则将缩略图暂时缓存一段时间。如果达到缓存时间，则删除缩略图。
    # 这是针对远程挂载的文件系统的优化，因为远程挂载的文件系统可能会在一段时间后不可用。
    cache_time: timedelta = timedelta(days=1)

    # 缩略图是否可用？非最新或者不存在时不可用。
    def is_outdated(self):
        # 获取路径下文件的创建时间与更新时间
        file_created_at_timestamp = os.path.getctime(self.path)
        file_updated_at_timestamp = os.path.getmtime(self.path)

        # 将时间戳转换为带有时区的 datetime 对象
        file_created_at = timezone.make_aware(datetime.fromtimestamp(file_created_at_timestamp))
        file_updated_at = timezone.make_aware(datetime.fromtimestamp(file_updated_at_timestamp))

        # 比较创建时间与更新时间是否相同
        return file_created_at == self.file_created_at and file_updated_at == self.file_updated_at

    # 缩略图是否存在？存在时可用。
    def thumbnail_exists(self):
        return self.thumbnail and self.file_created_at and self.file_updated_at and os.path.exists(self.thumbnail.path)

    # 获取并更新缩略图。（覆盖）
    # 如果文件不存在了，则将缩略图暂时缓存一段时间。如果达到缓存时间，则删除模型。
    def update_thumbnail(self):
        # 如果文件不存在，则将缩略图暂时缓存一段时间。如果达到缓存时间，则删除模型。
        if not os.path.exists(self.path):
            print("缩略图不存在")
            if self.thumbnail_exists() and abs(timezone.now() - self.file_updated_at) > self.cache_time:
                print("\t缩略图已经过期，删除之模型。")
                self.delete()
                return
            print("\t缩略图未过期，不删除模型。")
            return

        # 若存在，则更新缩略图。
        try:
            clip = VideoFileClip(self.path)
            time = clip.duration / 2  # 获取视频的中间帧作为缩略图

            # 在系统的临时目录中创建临时文件
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                thumbnail_path = f.name

            clip.save_frame(thumbnail_path, t=time)

            # 打开缩略图文件并保存到模型中
            with open(thumbnail_path, "rb") as f:
                self.thumbnail.save(thumbnail_path, File(f), save=True)
                os.remove(thumbnail_path)
        except Exception as e:
            print("更新缩略图遇到异常： ", e)

    def __str__(self):
        return f"[Thumb for {os.path.basename(self.path)}]"

    # 删除时，确保缩略图文件也被删除。
    def delete(self, *args, **kwargs):
        self.thumbnail.delete()
        super().delete(*args, **kwargs)

from lib import hash
import os
from django.db import models
from os.path import isdir


class MediaLibrary(models.Model):
    """
    这是媒体库的基类. 一个媒体库中可保存多个MediaUnit.
    根据MediaLibrary类型的不同,可以生成不同的MediaUnit.
    """

    root_nodes = models.ManyToManyField("FSNode")  # 媒体库的根节点们
    library_type = models.CharField(max_length=128, null=False)  # SHOWS, FILMS, IMAGES, MUSICS, BOOKS, FILES
    structure_type = models.CharField(max_length=128, null=False)  # "COMPLEX(自定义指定)", "FLAT(一个文件夹对应一个剧集)"

    def create_library(path, library_type="SHOWS", structure_type="FLAT"):
        """创建库."""
        node = path if path is FSNode else FSNode(path=path)  # Path可以输入为节点/字符串.
        return MediaLibrary(root_node=node, library_type=library_type, structure_type=structure_type)


class MediaUnit(models.Model):
    """
    媒体单位的元数据.
    一部剧, 一张保存在文件夹里的专辑, 一堆存在一个文件夹里的图片, 都可以被分别视为一个'MediaUnit'.
    MediaUnit是分类聚集的最小单位. 粒度再小一点,就是FSNode了. 用MediaUnit可以区分不同的聚集.
    另外,从IMDB进行刮削, MediaUnit也是最小单位.
    MediaUnit一定属于某个MediaLibrary.
    """

    # 每个媒体一定会属于一个库. 如果库没了,媒体Unit也会一起被删除.
    library = models.ForeignKey(MediaLibrary, on_delete=models.CASCADE, null=False, related_name="unit")
    path = models.CharField(max_length=512)  # 绝对路径
    nickname = models.CharField(max_length=512)  # 自定义别名. 由用户手动指定

    def get_basename(self):
        "获取文件夹名称."
        return os.path.basename(self.path)


# class TMDBMetadata(models.Model):
#     """
#     从TMDB获取的元数据.
#     """

#     tmdb_id = models.CharField()  # TheMovieDB上的id
#     is_locked = models.BooleanField()  # 是否锁定该元数据

#     localized_title = models.CharField()  # 剧集的本地化名称
#     original_title = models.CharField()  # 剧集的原本名称

#     date_added = models.DateField()
#     status = models.CharField()
#     community_rating = models.CharField()
#     overview = models.CharField()
#     release_date = models.DateField()
#     year = models.CharField()  # 发行年份
#     end_date = models.CharField()  # 截至年份

#     genres = models.ManyToManyField(to="GenresMetadata", related_name="tmdbmetadata")  # 流派
#     actors = models.ManyToManyField(to="ActorMetadata", related_name="tmdbmetadata")  # 演员
#     studio = models.ManyToManyField(to="StudioMetadata", related_name="tmdbmetadata")  # 工作室
#     keywords = models.ManyToManyField(to="KeywordMetadata", related_name="tmdbmetadata")  # 标签
#     metadata_download_language = models.CharField()  # 下载元数据偏好的语言
#     country = models.CharField()  # 国家


# class GenresMetadata(models.Model):
#     """流派元数据"""
#     title = models.CharField()


# class ActorMetadata(models.Model):
#     """演员元数据"""

#     name = models.CharField()
#     icon = models.ImageField()


# class KeywordMetadata(models.Model):
#     """标签元数据"""

#     title = models.CharField()


# class StudioMetadata(models.Model):
#     """工作室元数据"""

#     name = models.CharField()
#     icon = models.ImageField()


# 文件系统的节点树.
class FSNode(models.Model):
    """
    文件系统的映射节点. 用于供媒体库使用. 每当创建一个媒体库,就构建一颗映射树.
    映射树内的每个节点,对应着真实路径下的某个位置. 节点的属性并非实时更新的. 需要使用函数手动递归更新.
    """

    HASH_METHOD = "md5"  # "sha256"

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="child")  # 父节点
    path = models.CharField(max_length=512)  # 所指向的绝对路径

    # 文件元数据. 非实时, 需手动更新.
    meta_size = models.BigIntegerField(null=True, blank=True)
    meta_hash = models.CharField(max_length=512, null=True, blank=True)
    meta_last_modified_time = models.DateTimeField(null=True, blank=True)
    meta_last_created_time = models.DateTimeField(null=True, blank=True)

    # UNTESTED
    def get_child(self, child_name: str):
        """根据名称获取单层子节点"""
        for child in self.child.all():
            if child_name == os.path.basename(child.path):
                return child
        raise Exception("core::FSNode::get_child(): 错误!未能找到Child! 输入文件名为: " + child_name)

    def get_children(self, deep=False) -> set[str]:
        if deep == False:
            return set(self.child.all())
        else:
            # 返回当前节点的所有子节点的get_children()
            # 也就是当前所有子节点get_children的union
            # 如果是末端节点,那么get_children应该是empty
            if not os.path.isdir(self.path):
                return set([])
            result = set(self.child.all())

            for child_node in result:  # 遍历当前子节点:
                result = result.union(child_node.get_children(deep=True))
            return result

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

    def update_recursively(self, ttl: int = 10) -> None:
        """递归更新文件映射树."""
        if ttl <= 0:  # 确保自己没有抵达最大深度
            print("\t[WARN]抵达最大深度! 退出....")
            return
        elif not os.path.isdir(self.path):  # 确保自己是目录.
            # print("\t节点不可以被遍历，返回...", self)
            return

        try:
            # 为未追踪的路径创建节点
            for untracked_basename in self.get_untracked_basenames():
                node = FSNode(
                    path=os.path.join(self.path, untracked_basename),
                    parent=self,
                )
                node.save()

            # 移除丢失追踪的节点
            lost_track_nodes = self.get_lost_track_nodes()
            for n in lost_track_nodes:
                n.delete()

            # 保存自己
            self.save()

            # 尝试对自己的children迭代call.
            try:
                for child_node in self.get_children():
                    child_node.update_recursively(ttl - 1)
            except Exception as e:
                print("迭代遇到错误:", e)

            # 再次尝试保存
            self.save()
            # print(f"[info]节点更新完毕: {self.path}")

        # 遇到错误
        except Exception as e:
            print("异常发生(core::update_recursively):\n\t", e)
            return

    def update_metadata(self):
        """更新当前节点的元数据."""
        try:
            abs_path = self.path
            if isdir(abs_path):
                """是目录"""
                print("是目录.")

            else:
                """是文件"""
                print("是文件.计算.")
                meta_size = os.path.getsize(abs_path)
                meta_hash = hash.get_file_hash(file_abs_path=self.path)

                meta_last_modified_time = os.path.getmtime(self.path)
                meta_last_created_time = os.path.getctime(self.path)

        except Exception as e:
            print(f"更新元数据时遇到错误:{e}")

    def __str__(self):
        return str(self.path)

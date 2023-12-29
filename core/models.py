from lib import hash
import os
from django.db import models
from os.path import isdir


# 文件系统的节点树.
class FSNode(models.Model):
    """
    文件系统的映射节点. 用于供媒体库使用. 每当创建一个媒体库,就构建一颗映射树.
    映射树内的每个节点,对应着真实路径下的某个位置. 节点的属性并非实时更新的. 需要使用函数手动递归更新.
    """

    HASH_METHOD = "md5"  # "sha256"

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="child"
    )  # 父节点
    absolute_path = models.CharField(max_length=512)  # 所指向的绝对路径

    # 文件元数据. 非实时, 需手动更新.
    meta_size = models.BigIntegerField(null=True, blank=True)
    meta_hash = models.CharField(max_length=512, null=True, blank=True)
    meta_last_modified_time = models.DateTimeField(null=True, blank=True)
    meta_last_created_time = models.DateTimeField(null=True, blank=True)

    # UNTESTED
    def get_child(self, child_name: str):
        """根据名称获取单层子节点"""
        for child in self.child.all():
            if child_name == os.path.basename(child.absolute_path):
                return child
        raise Exception(
            "core::FSNode::get_child(): 错误!未能找到Child! 输入文件名为: " + child_name
        )

    def get_children(self, deep=False) -> set[str]:
        if deep == False:
            return set(self.child.all())
        else:
            # 返回当前节点的所有子节点的get_children()
            # 也就是当前所有子节点get_children的union
            # 如果是末端节点,那么get_children应该是empty
            if not os.path.isdir(self.absolute_path):
                return set([])
            result = set(self.child.all())

            for child_node in result:  # 遍历当前子节点:
                result = result.union(child_node.get_children(deep=True))
            return result

    def get_untracked_basenames(self):
        """获取未被追踪的文件的名称(basename)"""
        children_names = {
            os.path.basename(i.absolute_path) for i in self.get_children()
        }
        filenames_in_path = set(os.listdir(self.absolute_path))
        untracked = filenames_in_path - children_names
        return untracked

    def get_lost_track_nodes(self):
        """获取丢失跟踪的子节点"""
        children_names = {
            os.path.basename(i.absolute_path) for i in self.get_children()
        }
        filenames_in_path = set(os.listdir(self.absolute_path))
        lost_track = children_names - filenames_in_path
        return {self.get_child(i) for i in lost_track}

    def update_recursively(self, ttl: int = 10) -> None:
        """递归更新文件映射树."""
        if ttl <= 0:  # 确保自己没有抵达最大深度
            print("\t[WARN]抵达最大深度! 退出....")
            return
        elif not os.path.isdir(self.absolute_path):  # 确保自己是目录.
            # print("\t节点不可以被遍历，返回...", self)
            return

        try:
            # 为未追踪的路径创建节点
            for untracked_basename in self.get_untracked_basenames():
                node = FSNode(
                    absolute_path=os.path.join(self.absolute_path, untracked_basename),
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
            # print(f"[info]节点更新完毕: {self.absolute_path}")

        # 遇到错误
        except Exception as e:
            print("异常发生(core::update_recursively):\n\t", e)
            return

    def update_metadata(self):
        """更新当前节点的元数据."""
        try:
            abs_path = self.absolute_path
            if isdir(abs_path):
                """是目录"""
                print("是目录.")
                
            else:
                """是文件"""
                print("是文件.计算.")
                meta_size = os.path.getsize(abs_path)
                meta_hash = hash.get_file_hash(file_abs_path=self.absolute_path)

                meta_last_modified_time = os.path.getmtime(self.absolute_path)
                meta_last_created_time = os.path.getctime(self.absolute_path)

        except Exception as e:
            print(f"更新元数据时遇到错误:{e}")

    def __str__(self):
        return str(self.absolute_path)

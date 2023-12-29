import logging
from os import system
import os
import shutil

from django.test import TestCase
from core.models import FSNode


class FSNodeTest(TestCase):
    def test_fsnode(self):
        """尝试进行测试"""
        system("clear")
        TEST_PATH = "/home/zincles/TestCase/"
        TEST = True

        def reset_folder():
            # 移除当前文件,创建新文件夹
            shutil.rmtree(TEST_PATH)
            os.makedirs(TEST_PATH)

        reset_folder()

        # 创建测试节点node, 保存
        node = FSNode(absolute_path=TEST_PATH)
        node.save()
        print("创建测试节点:", node.absolute_path)

        # 初始化目录. 为目录里创建两个txt文件: txt1, txt2
        with open(os.path.join(TEST_PATH, "file1.txt"), "w") as file:
            file.write("Hello. File 1")
        with open(os.path.join(TEST_PATH, "file2.txt"), "w") as file:
            file.write("Hello. File 2")

        def get_child_str_set(deep=False):
            if deep == False:
                return set(
                    os.path.basename(child.absolute_path)
                    for child in node.get_children()
                )
            else:
                return set(
                    os.path.relpath(child.absolute_path, node.absolute_path)
                    for child in node.get_children(True)
                )

        def write_file(rela_path, content=""):
            with open(os.path.join(TEST_PATH, rela_path), "w") as file:
                file.write(content)

        def write_dir(rela_path):
            os.mkdir(os.path.join(TEST_PATH, rela_path))

        def get_all_node_in_memory():
            return set(node.absolute_path for node in FSNode.objects.all())

        ## 检查两次重复扫描结果是否相同?
        if TEST:
            # 更新扫描节点.
            node.update_recursively()
            result_1 = get_child_str_set()

            # 再次更新节点
            node.update_recursively()
            result_2 = get_child_str_set()

            print("首次更新:\n\t", result_1)
            print("二次更新:\n\t", result_2)

            if not (result_1 == result_2 == {"file1.txt", "file2.txt"}):
                raise Exception("错误!两次重复的扫描结果不相同!")

        ## 检查是否能识别文件的删除?
        if TEST:
            os.remove(os.path.join(TEST_PATH, "file1.txt"))
            node.update_recursively()
            result_3 = get_child_str_set()
            print("删除文件后:\n\t", result_3)
            if not (result_3 == {"file2.txt"}):
                raise Exception("删除段出错!扫描结果不符合!")

        # 检查是否节点全部被释放,防止泄漏 故障!不能测试深层目录!
        def memory_leak_test():
            if (set(FSNode.objects.all())) != (set(node.child.all()).union({node})):
                raise Exception("出现了节点的内存泄漏!")
            else:
                print("内存泄漏测试通过.")

        # 重置测试文件夹
        reset_folder()

        ## 检查是否能正确识别目录, 以及目录里的东西:

        if TEST:
            write_dir("FOLDER1")
            write_dir("FOLDER1/FOLDER2")

            write_file("file0.txt", "File 0")
            write_file("FOLDER1/file1.txt", "File 1")
            write_file("FOLDER1/FOLDER2/file2.txt", "FIle 2")

            node.update_recursively()
            print("深度查询:\n\t", get_child_str_set(True))

            if get_child_str_set(True) == {
                "FOLDER1",
                "FOLDER1/FOLDER2/file2.txt",
                "FOLDER1/FOLDER2",
                "file0.txt",
                "FOLDER1/file1.txt",
            }:
                print("深度查询测试通过")
            else:
                raise Exception("深度查询出错!")

            # 手动进行测试的部分. 完成.
            # # 确保删除目录更新正常.
            # print(get_all_node_in_memory())
            
            # shutil.rmtree(os.path.join(TEST_PATH, "FOLDER1"))
            # node.update_recursively()
            # print(get_all_node_in_memory())
            
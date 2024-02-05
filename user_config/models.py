from django.db import models
from django.contrib.auth.models import User
import os

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
    def set_favorate_path(self, name:str, path:str):
        path = os.path.abspath(path)
        
        # 读取favorite_paths作为字典, 写入键值对
        favorite_paths :dict = self.favorite_paths
        favorite_paths[name] = path
        
        # 保存
        self.favorite_paths = favorite_paths
        self.favorite_paths.save()
    
    ## 获取个人的所有收藏目录
    def get_favorate_paths(self, name:str):
        return self.favorite_paths[name]
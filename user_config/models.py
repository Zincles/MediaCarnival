from django.db import models
from django.contrib.auth.models import User


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

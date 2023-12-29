from django.apps import AppConfig

# 核心库. 包含了特殊的文件系统的定义

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
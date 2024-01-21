from django.contrib import admin
from .models import UserConfig


class UserConfigAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "language"]
    list_display_links = ["id", "user"]

    def __str__(self) -> str:
        return f"[UserConfig: {self.user.username}]"


admin.site.register(UserConfig, UserConfigAdmin)

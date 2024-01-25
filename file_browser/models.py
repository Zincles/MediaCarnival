from datetime import timedelta
import time
from django.db import models
import os
from moviepy.editor import VideoFileClip
from django.core.files import File
import tempfile
from datetime import datetime
from django.utils import timezone
# Create your models here.


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

    # 获取并更新缩略图。如果文件不存在了，则将缩略图暂时缓存一段时间。如果达到缓存时间，则删除缩略图。
    # 这是针对远程挂载的文件系统的优化，因为远程挂载的文件系统可能会在一段时间后不可用。
    # 该函数不进行原缩略图的可用性检验。无论存在与否都会覆盖。
    def update_thumbnail(self):
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

    def __str__(self):
        return f"[Thumb for {os.path.basename(self.path)}]"

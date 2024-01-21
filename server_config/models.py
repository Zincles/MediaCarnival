from django.db import models


class TmdbAccessToken(models.Model):
    """TheMovieDB的访问令牌"""

    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.value[:25] + "..."

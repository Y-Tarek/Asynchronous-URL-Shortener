from django.db import models
import random, string


class ShortenedURL(models.Model):
    original_url = models.URLField(unique=True)
    shortened_code = models.CharField(max_length=10, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.original_url:
            self.shortened_code = "".join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )
        return super().save(*args, **kwargs)

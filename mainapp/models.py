from django.conf import settings
from django.db import models
from hashids import Hashids


class Urls(models.Model):
    long_url = models.URLField(max_length=2000)
    short_url = models.CharField(max_length=5, blank=True)
    clicks = models.PositiveIntegerField(default=0)
    owner = models.CharField(max_length=200, default='AnonymousUser')
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Urls"

    def save(self, *args, **kwargs):
        super(Urls, self).save(*args, **kwargs)
        hashids = Hashids(salt=settings.HASHID_FIELD_SALT, min_length=5)
        self.short_url = hashids.encode(self.pk)
        super(Urls, self).save(*args, **kwargs)

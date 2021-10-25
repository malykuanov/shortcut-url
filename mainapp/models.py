from django.db import models


class Urls(models.Model):
    long_url = models.URLField(max_length=2000)
    short_url = models.CharField(max_length=5)
    clicks = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)

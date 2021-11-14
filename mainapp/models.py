from hashids import Hashids

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatechars


User = get_user_model()


def get_default_user():
    user, created = (User.objects
                         .get_or_create(username=settings.DEFAULT_USERNAME))
    if created:
        user.set_password(settings.DEFAULT_PASSWORD)
        user.save()
    return user.pk


class Urls(models.Model):
    long_url = models.URLField(max_length=2000)
    short_url = models.CharField(max_length=5, blank=True)
    clicks = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=get_default_user
    )
    time_create = models.DateTimeField(auto_now_add=True)
    time_last_click = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Urls"

    @property
    def long_url_truncate(self):
        return truncatechars(self.long_url, 50)

    def save(self, *args, **kwargs):
        super(Urls, self).save(*args, **kwargs)
        hashids = Hashids(salt=settings.HASHID_FIELD_SALT, min_length=5)
        self.short_url = hashids.encode(self.pk)
        super(Urls, self).save(*args, **kwargs)

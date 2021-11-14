from django.contrib import admin

from mainapp.models import Urls


class UrlsAdmin(admin.ModelAdmin):
    list_display = (
        'long_url_truncate', 'short_url', 'clicks',
        'owner', 'time_create', 'time_last_click'
    )
    list_display_links = ('long_url_truncate', 'short_url')
    search_fields = ('long_url', 'short_url')
    readonly_fields = [
        'long_url', 'short_url', 'clicks',
        'owner', 'time_create', 'time_last_click'
    ]


admin.site.register(Urls, UrlsAdmin)

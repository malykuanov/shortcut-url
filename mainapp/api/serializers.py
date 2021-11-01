from rest_framework import serializers

from mainapp.models import Urls


class UrlsSerializer(serializers.ModelSerializer):
    """List all Urls"""

    class Meta:
        model = Urls
        fields = ('long_url', 'short_url', 'clicks', 'time_create')


class CreateUrlSerializer(serializers.ModelSerializer):
    """Serializer for POST method"""

    class Meta:
        model = Urls
        fields = ('long_url', 'short_url', 'clicks', 'time_create')

    def save(self):
        long_url = self.validated_data.get('long_url')
        clicks = self.validated_data.get('clicks', 0)
        url = Urls(long_url=long_url, clicks=clicks)
        url.save()

from rest_framework import serializers

from mainapp.models import Urls


class UrlsSerializer(serializers.ModelSerializer):
    """List all Urls"""

    short_url = serializers.ReadOnlyField()
    clicks = serializers.ReadOnlyField()
    time_create = serializers.ReadOnlyField()
    time_last_click = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Urls
        exclude = ('id', )


class CreateUrlSerializer(serializers.ModelSerializer):
    """Serializer for POST method"""

    class Meta:
        model = Urls
        exclude = ('id', )

    def create(self, validated_data):
        long_url = validated_data.get('long_url')
        clicks = 0
        owner = self.context.get("request").user
        url = Urls(long_url=long_url, clicks=clicks, owner=owner)
        url.save()
        return url

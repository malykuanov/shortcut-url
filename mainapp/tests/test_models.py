from django.db import IntegrityError
from django.db.models import F
from django.test import TestCase

from mainapp.models import Urls


class UrlsModelTest(TestCase):
    """ Test module for Urls model """

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 11):
            url = Urls(long_url=f"example.com/{i}")
            url.save()
        cls.all_short_url = list(Urls.objects
                                     .values_list('short_url', flat=True))
        cls.all_url_owner = list(Urls.objects
                                     .values_list('owner', flat=True))

    def test_existence_short_url(self):
        self.assertNotIn("", self.all_short_url)

    def test_unique_short_url(self):
        self.assertEqual(
            len(self.all_short_url), len(set(self.all_short_url))
        )

    def test_increase_clicks(self):
        url = Urls.objects.filter(pk=1)
        url_clicks = url[0].clicks
        self.assertEqual(
            url.update(clicks=F('clicks') + 1), url_clicks + 1
        )

    def test_positive_clicks(self):
        with self.assertRaises(IntegrityError):
            Urls.objects.filter(pk=1).update(clicks=-10)

    def test_default_owner(self):
        self.assertEqual(
            {1}, set(self.all_url_owner)
        )
        self.assertEqual(Urls.objects.first().owner.username, 'default_user')

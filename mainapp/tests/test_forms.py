from django.test import TestCase

from mainapp.forms import ShortUrlForm, CheckClickUrlForm


class FormsUrlsTest(TestCase):
    """ Test module for Urls forms """

    def test_ShortUrlForm_valid(self):
        form = ShortUrlForm(data={'long_url': "example.com/test"})
        self.assertTrue(form.is_valid())

    def test_ShortUrlForm_invalid(self):
        form = ShortUrlForm(data={'long_url': "example.123"})
        self.assertFalse(form.is_valid())

    def test_CheckClickUrlForm_valid(self):
        form = CheckClickUrlForm(data={'short_url': "example.com/AbCdE"})
        short_url = ""
        if form.is_valid():
            short_url = form.check_correct_url(
                domain="example.com"
            )
        self.assertTrue(short_url)

    def test_CheckClickUrlForm_invalid(self):
        form = CheckClickUrlForm(data={'short_url': "example.com/123ABCde456"})
        short_url = ""
        if form.is_valid():
            short_url = form.check_correct_url(
                domain="example.com"
            )
        self.assertFalse(short_url)

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import resolve, reverse

from mainapp.models import Urls
from mainapp.views import (CheckClicks, ClicksCounter, Contact, HomePage,
                           ShortUrl, TermsOfService)


class UrlsViewsTest(TestCase):
    """ Test module for Urls views """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.User = get_user_model()
        cls.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }

    def test_home_page(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/index.html')
        self.assertEqual(resolve(url).func.view_class, HomePage)

    def test_shorturl_page(self):
        url = reverse("shorturl")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/shorturl.html')
        self.assertEqual(resolve(url).func.view_class, ShortUrl)

    def test_url_check_clicks_page(self):
        url = reverse("check_clicks")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/check_clicks.html')
        self.assertEqual(resolve(url).func.view_class, CheckClicks)

    def test_url_clicks_counter_page(self):
        url = reverse("clicks", args=["ABCDE"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/clicks_counter.html')
        self.assertEqual(resolve(url).func.view_class, ClicksCounter)

    def test_wrong_url_page(self):
        url = reverse("report")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/report.html')
        self.assertEqual(resolve(url).func.view_class, Contact)

    def test_contact_page(self):
        url = reverse("contact")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/contact.html')
        self.assertEqual(resolve(url).func.view_class, Contact)

    def test_terms_page(self):
        url = reverse("terms")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/terms_of_service.html')
        self.assertEqual(resolve(url).func.view_class, TermsOfService)

    def test_redirect_page(self):
        response = self.client.get(reverse("redirect_on_site", args=["ABCDE"]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        url = Urls(long_url="example.com")
        url.save()
        response = self.client.get(reverse("redirect_on_site",
                                           args=[url.short_url]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url.long_url)

    def test_dashboard_redirect_anon_and_auth_user(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/sign-in/?next=/dashboard/")
        self.User.objects.create_user(**self.credentials)
        self.client.post('/sign-in/', self.credentials, follow=True)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_delete_url_page(self):
        url = Urls(long_url="example.com/deleteme")
        url.save()
        self.assertTrue(Urls.objects.get(pk=1).long_url, "example.com/deleteme")
        response = self.client.post(reverse("delete_url", args=[url.pk]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Urls.objects.get(pk=1)

    def test_signin_page(self):
        self.User.objects.create_user(**self.credentials)
        response = self.client.post('/sign-in/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)
        self.assertRedirects(response, reverse("home"))

    def test_signup_page(self):
        response = self.client.post(reverse('sign-up'), data={
            'username': "testuser",
            'email': "test@gmail.com",
            'password1': "somesupersecretpassword",
            'password2': "somesupersecretpassword"
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.User.objects.create_user(**self.credentials)
        self.client.post('/sign-in/', self.credentials, follow=True)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

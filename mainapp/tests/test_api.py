import base64

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mainapp.api.serializers import UrlsSerializer
from mainapp.models import Urls


class RegistrationAPITest(APITestCase):
    """ Test module for Urls API """

    def setUp(self):
        self.data = {
            "username": "test_user",
            "password": "some_strong_password1"
        }

    def test_registration(self):
        # User registration test
        response = self.client.post("/api-auth/users/", self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Token acquisition test
        response = self.client.post("/api-auth/token/login/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UrlsAPITest(APITestCase):
    """ Test module for Urls API """

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 4):
            url = Urls(long_url=f"example.com/{i}")
            url.save()

        cls.list_url = reverse("mainapp:urls")
        cls.one_url = reverse(
            "mainapp:url",
            kwargs={"short_url": Urls.objects.get(pk=1).short_url}
        )

    def setUp(self):
        self.user = User.objects.create_user(username="test_name",
                                             password="some_strong_password")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_urls_authenticated_by_token(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.one_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_urls_authenticated_by_basic_auth(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Basic  ' + base64.b64encode(
                b'test_name:some_strong_password').decode("ascii")
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.one_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_urls_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.one_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_url(self):
        valid_url = "http://example.com/new"
        invalid_url = "example.com/new"
        response = self.client.post(self.list_url, {"long_url": valid_url})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.list_url, {"long_url": invalid_url})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_urls_retrieve(self):
        valid_url = "http://example.com/new"
        for _ in range(0, 5):
            self.client.post(self.list_url, {"long_url": valid_url})
        response = self.client.get(self.list_url)
        urls = Urls.objects.filter(owner=User.objects.get(username='test_name').pk).order_by('-pk')
        serializer = UrlsSerializer(urls, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_detail_retrieve(self):
        response = self.client.get(self.one_url)
        self.assertEqual(response.data["long_url"], "example.com/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_clicks_url(self):
        data = {
          "long_url": "http://example.com/1",
          "short_url": Urls.objects.get(pk=1).short_url,
          "clicks": 666,
          "time_create": Urls.objects.get(pk=1).time_create,
          "time_last_clicks": "",
          "owner": Urls.objects.get(pk=1).owner
        }
        serializer = UrlsSerializer(data)
        response = self.client.put(self.one_url, data)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Urls.objects.get(pk=1).clicks, 666)

    def test_patch_long_url(self):
        response = self.client.patch(self.one_url, {"long_url": "http://example.com/test_patch_url"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Urls.objects.get(pk=1).long_url, "http://example.com/test_patch_url")

    def test_immutability_short_link(self):
        response = self.client.patch(self.one_url, {"short_url": "AbCdE"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(Urls.objects.get(pk=1).short_url, "AbCdE")

    def test_delete_url(self):
        response = self.client.delete(self.one_url)
        url = Urls.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(url, None)


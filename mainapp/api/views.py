from django.http import Http404, HttpResponse
from rest_framework import permissions
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication)
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp.models import Urls

from .serializers import CreateUrlSerializer, UrlsSerializer


class UrlsListView(APIView):
    """Show url list"""

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        urls = (Urls.objects
                    .filter(owner=self.request.user)
                    .order_by('-time_create'))
        serializer = UrlsSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        url = CreateUrlSerializer(
            data=request.data,
            context={'request': request}
        )
        if url.is_valid():
            url.save()
            return Response(url.data, status=201)
        return Response(url.errors, status=400)


class UrlDetailView(APIView):
    """Show url detail"""

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, short_url):
        try:
            url = Urls.objects.get(short_url=short_url)
            if url.owner != self.request.user:
                raise Http404
            return url
        except Urls.DoesNotExist:
            raise Http404

    def get(self, request, short_url):
        url = self.get_object(short_url)
        serializer = UrlsSerializer(url)
        return Response(serializer.data, status=200)

    def put(self, request, short_url):
        url = self.get_object(short_url)
        serializer = UrlsSerializer(url, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, short_url):
        url = self.get_object(short_url)
        serializer = UrlsSerializer(url, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, short_url):
        url = self.get_object(short_url)
        url.delete()
        return Response(status=204)

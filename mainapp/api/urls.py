from django.urls import path

from .views import UrlsListView, UrlDetailView


app_name = "mainapp"

urlpatterns = [
    path('urls/', UrlsListView.as_view()),
    path('urls/<slug:short_url>', UrlDetailView.as_view()),
]
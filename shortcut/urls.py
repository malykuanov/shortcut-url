from django.contrib import admin
from django.urls import path

from mainapp.views import index, shorturl, redirect_on_site, check_clicks, \
    clicks_counter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('shorturl/', shorturl, name='shorturl'),
    path('url-click-counter/', check_clicks, name='check_clicks'),
    path('url-click-counter/<slug:short_url>', clicks_counter, name='clicks'),
    path('<slug:short_url>/', redirect_on_site, name='redirect_on_site'),
]

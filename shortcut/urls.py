from django.contrib import admin
from django.urls import path

from mainapp.views import index, shorturl, redirect_on_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('shorturl/', shorturl, name='shorturl'),
    path('<slug:short_url>/', redirect_on_site, name='redirect_on_site'),
]

from django.contrib import admin
from django.urls import path

from mainapp.views import index, shorturl

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('shorturl/', shorturl, name='shorturl')
]

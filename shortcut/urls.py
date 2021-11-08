from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('djoser.urls')),
    path('api-auth/', include('djoser.urls.authtoken')),
    path('api/v1/', include('mainapp.api.urls')),
    path('', include('mainapp.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

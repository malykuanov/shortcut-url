from django.urls import path

from .views import (CheckClicks, ClicksCounter, Contact, HomePage,
                    RedirectOnSite, ShortUrl, TermsOfService)

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('shorturl/', ShortUrl.as_view(), name='shorturl'),
    path('url-click-counter/', CheckClicks.as_view(), name='check_clicks'),
    path('url-click-counter/<slug:short_url>',
         ClicksCounter.as_view(), name='clicks'),
    path('report-wrong-url/', Contact.as_view(), name='report'),
    path('terms-of-service/', TermsOfService.as_view(), name='terms'),
    path('contact/', Contact.as_view(), name='contact'),
    path('<slug:short_url>/', RedirectOnSite.as_view(),
         name='redirect_on_site'),
]
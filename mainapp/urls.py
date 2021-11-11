from django.urls import path

from .views import (logout_user, CheckClicks, ClicksCounter, Contact,
                    Dashboard, HomePage, LoginUser, RedirectOnSite,
                    RegistrationUser, ShortUrl, TermsOfService, DeleteUrl)


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('sign-in/', LoginUser.as_view(), name='sign-in'),
    path('sign-up/', RegistrationUser.as_view(), name='sign-up'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('delete-url/<int:pk>', DeleteUrl.as_view(), name='delete_url'),
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

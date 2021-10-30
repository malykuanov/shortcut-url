import re

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from mainapp.forms import (ShortUrlForm, CheckClickUrlForm,
                           ReportWrongUrlForm, ContactForm)
from mainapp.models import Urls


def index(request):
    form = ShortUrlForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            url = form.save()
            request.session['short_url'] = url.short_url
            return redirect('shorturl')

    return render(request, 'mainapp/index.html', {'form': form})


class ShortUrl(TemplateView):
    template_name = 'mainapp/shorturl.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        short_url = self.request.session.get('short_url')
        context['url'] = Urls.objects.filter(short_url=short_url).first()
        return context


class RedirectOnSite(View):

    def dispatch(self, request, *args, **kwargs):
        url = Urls.objects.filter(short_url=self.kwargs['short_url']).first()
        if url:
            (Urls.objects
                 .filter(short_url=url.short_url)
                 .update(clicks=F('clicks') + 1))
            return HttpResponseRedirect(url.long_url)
        else:
            return redirect('home')


class CheckClicks(FormView):
    template_name = 'mainapp/check_clicks.html'
    form_class = CheckClickUrlForm

    def form_valid(self, form):
        short_url = form.check_correct_url(
            domain=str(get_current_site(self.request))
        )
        if short_url:
            return redirect('clicks', short_url)
        else:
            messages.error(
                self.request,
                "Ссылка указана неверно. Проверьте домен и короткий URL"
            )
            return super().form_valid(form)

    def get_success_url(self):
        return self.request.path
    

def clicks_counter(request, short_url):
    url = Urls.objects.filter(short_url=short_url).first()
    clicks = 0
    if url:
        clicks = url.clicks

    return render(request,
                  'mainapp/clicks_counter.html',
                  {'clicks': clicks})


class ReportWrongUrl(FormView):
    template_name = 'mainapp/report.html'
    form_class = ReportWrongUrlForm

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Сообщение отправлено')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class TermsOfService(TemplateView):
    template_name = 'mainapp/terms_of_service.html'


class Contact(FormView):
    template_name = 'mainapp/contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Сообщение отправлено')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path

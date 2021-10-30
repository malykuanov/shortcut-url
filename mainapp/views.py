import re

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
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


def shorturl(request):
    short_url = request.session.get('short_url')
    url = Urls.objects.filter(short_url=short_url).first()

    return render(request, 'mainapp/shorturl.html', {'url': url})


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


def check_clicks(request):
    form = CheckClickUrlForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            url = form.cleaned_data['short_url']
            domain = str(get_current_site(request))
            regex = r'^' + domain + r'.\w{5}$'
            if re.match(regex, url):
                short_url = url.split('/')[1]
                return redirect('clicks', short_url)
            else:
                form.add_error(
                    None,
                    "Ссылка указана неверно. Проверьте домен и короткий URL"
                )

    return render(request, 'mainapp/check_clicks.html', {'form': form})


def clicks_counter(request, short_url):
    url = Urls.objects.filter(short_url=short_url).first()
    clicks = 0
    if url:
        clicks = url.clicks

    return render(request,
                  'mainapp/clicks_counter.html',
                  {'clicks': clicks})


def report_wrong_url(request):
    form = ReportWrongUrlForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            subject = form.cleaned_data['short_url']
            message = form.cleaned_data['comment']

            send_mail(
                subject,
                message,
                settings.ADMIN_MAIL,
                [settings.ADMIN_MAIL]
            )
            messages.success(request, 'Сообщение отправлено')
            form = ReportWrongUrlForm()

            return render(request, 'mainapp/report.html', {'form': form})

    return render(request, 'mainapp/report.html', {'form': form})


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

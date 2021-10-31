from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView, TemplateView

from mainapp.forms import (ShortUrlForm, CheckClickUrlForm,
                           ReportWrongUrlForm, ContactForm)
from mainapp.models import Urls


class HomePage(FormView):
    form_class = ShortUrlForm
    template_name = 'mainapp/index.html'
    success_url = '/shorturl/'

    def form_valid(self, form):
        url = form.save()
        self.request.session['short_url'] = url.short_url
        return super().form_valid(form)


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
    

class ClicksCounter(TemplateView):
    template_name = 'mainapp/clicks_counter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = Urls.objects.filter(short_url=self.kwargs['short_url']).first()
        context['clicks'] = url.clicks if url else 0
        return context


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

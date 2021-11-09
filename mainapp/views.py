from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import resolve, reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from mainapp.forms import (CheckClickUrlForm, ContactForm,
                           RegistrationUserForm, ShortUrlForm)
from mainapp.models import Urls


class HomePage(FormView):
    form_class = ShortUrlForm
    template_name = 'mainapp/index.html'

    def form_valid(self, form):
        url = form.save()
        # Using sessions to save the last
        # 5 shortened links for an anonymous user
        self.request.session.setdefault('short_url', [])
        if len(self.request.session['short_url']) == 5:
            del self.request.session['short_url'][0]
        self.request.session['short_url'].append(url.short_url)
        self.request.session.modified = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shorturl')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_url = self.request.session.get('short_url', [])
        context['list_url'] = Urls.objects.filter(short_url__in=list_url)
        return context


class ShortUrl(TemplateView):
    template_name = 'mainapp/shorturl.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        short_url = self.request.session.get('short_url')[-1]
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
            return redirect('check_clicks')


class ClicksCounter(TemplateView):
    template_name = 'mainapp/clicks_counter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = Urls.objects.filter(short_url=self.kwargs['short_url']).first()
        context['clicks'] = url.clicks if url else 0
        return context


class Contact(FormView):
    wrong_url_template_name = 'mainapp/report.html'
    contact_template_name = 'mainapp/contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'Сообщение отправлено')
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path

    def get_template_names(self):
        if resolve(self.request.path_info).url_name == 'report':
            return [self.wrong_url_template_name]
        else:
            return [self.contact_template_name]


class TermsOfService(TemplateView):
    template_name = 'mainapp/terms_of_service.html'


class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'mainapp/registration.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'mainapp/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')

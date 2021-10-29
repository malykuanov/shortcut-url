from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render

import re

from mainapp.forms import ShortUrlForm, CheckClickUrlForm
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


def redirect_on_site(request, short_url):
    url = Urls.objects.filter(short_url=short_url).first()
    if url:
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

    return render(request, 'mainapp/click_counter.html', {'form': form})


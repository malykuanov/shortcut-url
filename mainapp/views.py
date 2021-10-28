from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from mainapp.forms import ShortUrlForm
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

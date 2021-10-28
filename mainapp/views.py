from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from mainapp.forms import ShortUrlForm


def index(request):
    form = ShortUrlForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'mainapp/index.html', {'form': form})

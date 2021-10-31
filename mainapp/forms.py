import re

from django import forms
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from mainapp.models import Urls


class ShortUrlForm(forms.ModelForm):
    class Meta:
        model = Urls
        fields = ['long_url']
        widgets = {
            'long_url': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Укажите ссылку для сокращения ...'})
        }


class CheckClickUrlForm(forms.Form):
    short_url = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input-clicks',
            'placeholder': 'Укажите здесь короткую ссылку ...'
        })
    )

    def check_correct_url(self, domain):
        """Checking url for a schema: {domain}/{short_url}

        Keyword argument:
        domain (str) -- site domain without port

        Returned value:
        short_url (str) - if url matches the schema
        false (bool) - if url incorrect
        """

        url = self.cleaned_data.get('short_url')
        regex = r'^' + domain + r'.\w{5}$'
        if re.match(regex, url):
            return url.split('/')[1]
        else:
            return False


class ReportWrongUrlForm(forms.Form):
    short_url = forms.CharField(max_length=100)
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'cols': 20,
            'rows': 5
        })
    )

    def send_email(self):
        send_mail(
            self.cleaned_data['short_url'],
            self.cleaned_data['comment'],
            settings.ADMIN_MAIL,
            [settings.ADMIN_MAIL]
        )


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'cols': 20,
            'rows': 5
        })
    )

    def send_email(self):
        send_mail(
            self.cleaned_data['name'],
            self.cleaned_data['message'],
            self.cleaned_data['email'],
            [settings.ADMIN_MAIL]
        )

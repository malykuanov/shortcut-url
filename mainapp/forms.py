import re

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'cols': 20,
            'rows': 5
        })
    )

    def send_email(self):
        send_mail(
            subject=self.cleaned_data['subject'],
            message=(
                'From= '
                + self.cleaned_data['email']
                + ' Message='
                + self.cleaned_data['message']
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_MAIL]
        )


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput
    )
    email = forms.CharField(
        label='Адрес электронной почты',
        widget=forms.EmailInput
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

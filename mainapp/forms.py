from django import forms

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


class ReportWrongUrlForm(forms.Form):
    short_url = forms.CharField(max_length=100)
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'cols': 20,
            'rows': 5
        })
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

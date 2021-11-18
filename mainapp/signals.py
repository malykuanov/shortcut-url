from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid=settings.HASHID_FIELD_SALT)
def send_email_for_new_user(sender, instance, **kwargs):
    if kwargs['created']:
        context = {'username': instance.username}
        template = render_to_string(
            'mainapp/registration_email.html',
            context=context
        )
        send_mail(
            subject='Благодарим за регистрацию!',
            message=template,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=template,
        )

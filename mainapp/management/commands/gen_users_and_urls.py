from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from mainapp.models import Urls


class Command(BaseCommand):
    help = 'Генерирует пользователей и URLs'

    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            '--total',
            type=int,
            help='Количество создаваемых пользователей'
        )
        parser.add_argument(
            '-u',
            '--urls',
            type=int,
            help='Количество создаваемых urls для пользователя'
        )
        parser.add_argument(
            '-show',
            '--show_existing',
            action='store_true',
            default=False,
            help='Показать существующих пользователей и кол-во urls',
        )
        parser.add_argument(
            '-a',
            '--admin',
            action='store_true',
            default=False,
            help='Создание учетной записи администратора'
        )

    def handle(self, *args, **options):
        User = get_user_model()

        urls_count = options['urls'] if options['urls'] else 1

        if options['total']:
            for number in range(options['total']):
                user = User.objects.create_user(
                    username=get_random_string(),
                    email="",
                    password=settings.DEFAULT_PASSWORD
                )
                for i in range(urls_count):
                    url = Urls(
                        long_url=f"http://example.com/{user}/{i}",
                        owner=user
                    )
                    url.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully create user {user} with {urls_count} Urls'
                    )
                )
            self.stdout.write(self.style.MIGRATE_HEADING('All done'))

        if options['urls'] and not options['total']:
            # Create anonymous users
            for i in range(urls_count):
                url = Urls(
                    long_url=f"http://example.com/{get_random_string()}",
                )
                url.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully create {urls_count} URLs for @default_user'
                )
            )

        if options['show_existing']:
            total_users = User.objects.all().count()
            total_urls = 0

            for user in User.objects.all():
                urls_count = Urls.objects.filter(owner=user).count()
                total_urls += urls_count
                self.stdout.write(
                    self.style.SUCCESS(
                        f'User = {user.username}, urls = {urls_count}'
                    )
                )
            self.stdout.write(
                self.style.NOTICE(
                    f'\nTotal users = {total_users}, Total urls = {total_urls}'
                )
            )

        if options['admin']:
            if User.objects.filter(username=settings.ADMIN_DEFAULT_NAME):
                username = get_random_string()
            else:
                username = settings.ADMIN_DEFAULT_NAME
            User.objects.create_superuser(
                username=username,
                email='',
                password=settings.ADMIN_DEFAULT_PASSWORD
            )
            self.stdout.write(
                self.style.NOTICE('The administrator has been created!')
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Username = {username}'
                )
            )

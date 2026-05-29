import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from core.models import UserProfile


class Command(BaseCommand):
    help = 'Ensure the configured superuser exists, is active, and can log in.'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            raise CommandError('DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD must be set.')

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})

        user.email = email
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        UserProfile.objects.get_or_create(user=user)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created superuser account: {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated superuser account: {username}'))

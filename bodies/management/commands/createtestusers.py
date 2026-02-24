from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from bodies.models import Profile

USERS = [
    ('admin', 'admin', 'admin'),
    ('editor', 'editor', 'editor'),
    ('user', 'user', 'authorized'),
    ('guest', 'guest', 'unauthorized'),
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for username, password, role in USERS:
            user, _ = User.objects.get_or_create(username=username, defaults={'password': '!'})
            if user.check_password(password) is False:
                user.set_password(password)
                user.save()
            Profile.objects.update_or_create(user=user, defaults={'role': role})
            self.stdout.write(f'{username} / {password} / {role}')

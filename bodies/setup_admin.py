
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

from bodies.models import Profile

admin_user = User.objects.get(username='admin')

admin_user.set_password('admin')
admin_user.save()

profile, created = Profile.objects.get_or_create(
    user=admin_user,
    defaults={'role': 'admin'}
)

if created:
    print("админ создан")

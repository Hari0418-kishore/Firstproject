import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstproject.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("cinema", "harikishoretm@gmail.com", "12345")
    print("Superuser created")
else:
    print("Superuser already exists")

# core/management/commands/create_production_superuser.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a superuser for production using environment variables."

    def handle(self, *args, **options):
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        username = os.getenv("ADMIN_USERNAME", email.split("@")[0])

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "ADMIN_EMAIL and ADMIN_PASSWORD must be set in environment variables."
                )
            )
            return

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email, username=username, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created superuser: {email}")
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    f"Superuser with email {email} already exists."
                )
            )

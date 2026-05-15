import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import UserProfile


class Command(BaseCommand):
    help = "Create or update the default administrator account."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_ADMIN_USERNAME", "admin")
        password = os.getenv("DJANGO_ADMIN_PASSWORD", "zxczxc123")
        email = os.getenv("DJANGO_ADMIN_EMAIL", "admin@example.com")

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": "Администратор",
                "last_name": "Системы",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={"role": "admin", "phone": "+7 (495) 780-39-90"},
        )
        if profile.role != "admin":
            profile.role = "admin"
            profile.save(update_fields=["role"])

        status = "created" if created else "updated"
        profile_status = "created" if profile_created else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"Admin user '{username}' {status}; profile {profile_status}."
            )
        )

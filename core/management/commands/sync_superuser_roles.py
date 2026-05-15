"""
Management command: sync_superuser_roles

Assigns the 'admin' role in UserProfile to all existing superusers
who do not yet have a profile or whose profile role is not 'admin'.

Usage:
    python manage.py sync_superuser_roles
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import UserProfile


class Command(BaseCommand):
    help = (
        "Create or update UserProfile for all superusers and set their role to 'admin'."
    )

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        updated = 0
        created = 0

        for user in superusers:
            profile, was_created = UserProfile.objects.get_or_create(
                user=user, defaults={"role": "admin"}
            )
            if was_created:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  [created] Profile for '{user.username}' with role='admin'"
                    )
                )
            elif profile.role != "admin":
                profile.role = "admin"
                profile.save(update_fields=["role"])
                updated += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  [updated] '{user.username}' role set to 'admin'"
                    )
                )
            else:
                self.stdout.write(
                    f"  [ok]      '{user.username}' already has role='admin'"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone: {created} profile(s) created, {updated} profile(s) updated."
            )
        )

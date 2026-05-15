from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Auto-create a UserProfile whenever a new User is saved.
    - Superusers get role='admin'
    - Staff (but not superuser) get role='methodist'
    - Everyone else gets role='applicant'
    """
    if created:
        role = "applicant"
        if instance.is_superuser:
            role = "admin"
        elif instance.is_staff:
            role = "methodist"
        UserProfile.objects.get_or_create(user=instance, defaults={"role": role})
    else:
        # If a user was upgraded to superuser after creation, sync the profile role
        if instance.is_superuser:
            UserProfile.objects.filter(user=instance).update(role="admin")

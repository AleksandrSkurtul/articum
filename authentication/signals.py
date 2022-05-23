from django.dispatch import receiver

from djoser.signals import user_registered

from accounts.models import UserAccount


@receiver(user_registered)
def create_related_profile(user, **kwargs):
    UserAccount.objects.create(user=user)

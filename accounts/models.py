from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    # is_patient = models.BooleanField(default=False)
    # is_doctor = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, blank=True, null=True)
    # age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Client(models.Model):
    user = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    # age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email

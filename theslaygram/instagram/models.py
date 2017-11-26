from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Q, signals
from django.dispatch import receiver
# Create your models here.
Gender_Choices = (
    ('F', 'female'),
    ('M', 'male'),
    ('Both', 'both'),
    ('None', 'non-specified'),
)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    portfolio = models.CharField(max_length=500, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    gender = models.CharField(
        max_length=30, choices=Gender_Choices, default='None', blank=True)
    philosophy = models.TextField(max_length=500, blank=True)


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)

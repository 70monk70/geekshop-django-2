from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)

    activation_key = models.CharField(max_length=128, blank=True)

    def activation_key_expired(self):
        return now() - self.date_joined > timedelta(hours=48)


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'


    user = models.OneToOneField(
        User,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )

    country = models.CharField(verbose_name='страна', max_length=128, blank=True)

    current_city = models.CharField(verbose_name='текущий город', max_length=128, blank=True)

    gender = models.CharField(verbose_name='пол', max_length=1, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

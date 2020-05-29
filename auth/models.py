import os
import time

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator

from .validators import phone_validator


def user_image_upload_location(instance, filename):
    filename, extension = os.path.splitext(filename)
    return f'users/{instance.username}{time.time()}{extension}'


class User(AbstractUser):
    email = models.EmailField('email address', unique=True, blank=False)
    phone = models.CharField('phone number', validators=(
        phone_validator,), blank=True, null=False)
    image = models.ImageField(
        'profile photo', blank=True, null=True, upload_to=user_image_upload_location)
    birth_date = models.DateField('birth date', blank=True, null=True)
    city = models.ForeignKey('City', related_name='user',
                             on_delete=models.SET_NULL, blank=True, null=True)
    address = models.TextField('address',validators=(MaxLengthValidator(256),), blank=True)


class City(models.Model):
    name = models.CharField('city name')

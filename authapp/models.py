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
    email = models.EmailField(
        'email address', unique=True, null=False, blank=False)
    phone = models.CharField('phone number', max_length=11, validators=(
        phone_validator,), blank=True, null=True, unique=True)
    image = models.ImageField(
        'profile photo', blank=True, null=True, upload_to=user_image_upload_location)
    birth_date = models.DateField('birth date', blank=True, null=True)
    city = models.ForeignKey('City', related_name='users',
                             on_delete=models.SET_NULL, blank=True, null=True)
    address = models.TextField('address', validators=(
        MaxLengthValidator(256),), blank=True, null=False)

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username


class City(models.Model):
    name = models.CharField('city name', max_length=30, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

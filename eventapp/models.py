import os
import time

from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator


def event_image_upload_location(instance, filename):
    filename, extension = os.path.splitext(filename)
    return f'events/{instance.username}{time.time()}{extension}'


class Event(models.Model):
    title = models.CharField('title', max_length=30, blank=False)
    image = models.ImageField(
        'image', blank=True, null=True, upload_to=event_image_upload_location)
    description = models.TextField('description', validators=(
        MaxLengthValidator(256),), blank=True, null=False)
    start_time = models.DateTimeField('start time', blank=False)
    end_time = models.DateTimeField('end time', blank=False)
    address = models.TextField('address', validators=(
        MaxLengthValidator(256),), blank=True, null=False)
    tags = models.TextField('tags', validators=(
        MaxLengthValidator(256),), blank=True, null=False)
    # ----------------------- relations ------------------------------
    event_type = models.ForeignKey(
        'EventType', related_name='events', on_delete=models.CASCADE, blank=False)
    event_category = models.ForeignKey(
        'EventCategory', related_name='events', on_delete=models.CASCADE, blank=False)
    city = models.ForeignKey('authapp.City', related_name='events',
                             on_delete=models.CASCADE, blank=True, null=True)
    tickets = models.ManyToManyField(
        'Ticket', related_name='events', on_delete=models.CASCADE, blank=False)


class Ticket(models.Model):
    title = title = models.CharField('title', max_length=30, blank=False)
    description = models.TextField('description', validators=(
        MaxLengthValidator(256),), blank=True, null=False)
    capcity = models.PositiveIntegerField(
        'capacity', validators=(MinValueValidator(1),), blank=False)
    price = models.PositiveIntegerField(
        'price', blank=False)


class EventType(models.Model):
    name = models.CharField('type', unique=True,
                            max_length=30, blank=False, null=False)


class EventCategory(models.Model):
    name = models.CharField('category', unique=True,
                            max_length=30, blank=False, null=False)

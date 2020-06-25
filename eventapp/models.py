import os
import time

from django.db import models
from django.db.models import F
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.core.exceptions import FieldError

from .helper import generate_register_id


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
        'Ticket', related_name='events', blank=False)
    owner = models.ForeignKey(
        'authapp.User', related_name='created_events', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Ticket(models.Model):
    title = title = models.CharField('title', max_length=30, blank=False)
    description = models.TextField('description', validators=(
        MaxLengthValidator(256),), blank=True, null=False)
    capcity = models.PositiveIntegerField(
        'capacity', validators=(MinValueValidator(1),), blank=False)
    price = models.PositiveIntegerField(
        'price', blank=False)
    registered_users = models.ManyToManyField(
        'authapp.User', through='Register', related_name='tickets')

    def __str__(self):
        return self.title

    def __repr__(self):
        return title


class Register(models.Model):

    class Conditions:
        REGISTERED = 1
        CANCELED = 2

    condtion_choices = (
        (Conditions.REGISTERED, 'registered'),
        (Conditions.CANCELED, 'canceled'),
    )
    registration_id = models.CharField(
        'registration id', max_length=100, blank=True, null=False)
    user = models.ForeignKey(
        'authapp.User', related_name='register', on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        'Ticket', related_name='register', on_delete=models.CASCADE)
    condition = models.PositiveSmallIntegerField(
        'condition', choices=condtion_choices, blank=True, null=False)
    register_time = models.DateTimeField(
        'register time', auto_now_add=True, blank=True, null=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.ticket.capcity <= 0:
                raise FieldError('there isn\'t any capcity to register user')
            self.registration_id = generate_register_id(self.user, self.ticket)
            self.condition = Conditions.REGISTERED
            self.ticket.update(capcity=F('capcity')-1)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} | {self.ticket.title}'

    def __repr__(self):
        return f'{self.user.username} | {self.ticket.title}'


class EventType(models.Model):
    name = models.CharField('type', unique=True,
                            max_length=30, blank=False, null=False)

    def __str__(self):
        return name

    def __repr__(self):
        return name


class EventCategory(models.Model):
    name = models.CharField('category', unique=True,
                            max_length=30, blank=False, null=False)

    def __str__(self):
        return name

    def __repr__(self):
        return name

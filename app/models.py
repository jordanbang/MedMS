from django.db import models
from django.contrib.auth.models import User
# Create your models here.

DAYS_OF_WEEK = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
]


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='user', unique=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class Availability(models.Model):
    doctor = models.ForeignKey(Doctor)
    day = models.IntegerField(choices=DAYS_OF_WEEK, db_index=True)
    start = models.TimeField(db_index=True)
    end = models.TimeField(db_index=True)


class PatientRequests(models.Model):
    patient = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    open = models.BooleanField(db_index=True)


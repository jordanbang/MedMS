from django.db import models
from django.contrib.auth.models import User
# Create your models here.

DAYS_OF_WEEK = [
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday')
]


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='user', unique=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    last_modified = models.DateTimeField(auto_now=True)


class Availability(models.Model):
    doctor = models.ForeignKey(Doctor)
    day = models.CharField(choices=DAYS_OF_WEEK, db_index=True, max_length=3)
    start = models.TimeField(db_index=True)
    end = models.TimeField(db_index=True)
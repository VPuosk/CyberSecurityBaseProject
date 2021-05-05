import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Generic posting for creating SQL injection issue
class Post(models.Model):
    header = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    time = models.DateTimeField()

    def __str__(self):
        return self.header

    def postedWithinAWeek(self):
        return self.time >= timezone.now() - datetime.timedelta(days=7)

# Personal posting for creating access control issue
class Note(models.Model):
    header = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.header
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    header = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    time = models.DateTimeField()

    def __str__(self):
        return self.header

    def postedWithinAWeek(self):
        return self.time >= timezone.now() - datetime.timedelta(days=7)
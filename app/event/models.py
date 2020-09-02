from django.db import models


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=48)
    image = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

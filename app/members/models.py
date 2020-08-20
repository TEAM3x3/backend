from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('N', 'None'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    img_profile = models.ImageField(upload_to='user', blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=False)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    birthdate = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

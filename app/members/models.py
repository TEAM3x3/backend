from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    password = models.CharField(max_length=15, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False)
    nicname = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    # password_check = models.CharField(max_length=15, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

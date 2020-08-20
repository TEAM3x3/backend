from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    password = models.CharField(max_length=15, blank=False, null=False)
    phone = models.CharField(max_length=11, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False)
    nicname = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(max_length=11, null=True)
    address = models.TextField(null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')

    # password_check = models.CharField(max_length=15, blank=False, null=False)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.is_superuser == False:
    #         print(self.password)
    #         self.set_password(self.password)
    #         self.save()
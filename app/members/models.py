from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    )
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES)

    phone = models.CharField('핸드폰 번호', max_length=15)
    email = models.EmailField(unique=True, blank=False)
    address = models.CharField(max_length=200)
    nickname = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(max_length=11, null=True)

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')


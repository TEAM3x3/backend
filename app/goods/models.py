from django.db import models


# Create your models here.
class Goods(models.Model):
    img = models.ImageField(upload_to='goods')
    title = models.CharField(max_length=30)


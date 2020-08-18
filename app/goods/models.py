from django.db import models

# Create your models here.
import goods
from goods.crawling import crawling


class Goods(models.Model):
    img = models.ImageField(upload_to='goods')
    title = models.CharField(max_length=30)
    short_desc = models.CharField(max_length=50)
    price = models.IntegerField()
    goods_each = models.CharField(max_length=24, null=True, )
    each_weight = models.CharField(max_length=24, null=True, )
    transfer = models.CharField(max_length=24, null=True, )
    packing = models.CharField(max_length=64, null=True, )
    origin = models.CharField(max_length=48, null=True, )
    allergy = models.CharField(max_length=126, null=True, )
    info = models.CharField(max_length=126, null=True, )
    limit = models.CharField(max_length=64, null=True, )

    @staticmethod
    def get_crawling():
        crawling()

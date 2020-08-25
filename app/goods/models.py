from django.db import models

# Create your models here.
import goods
from goods.crawling import crawling


def goods_img_path(instance, filename):
    filename = filename.split('media/')
    print(filename[1])
    return filename[1]


def goods_info_img_path(instance, filename):
    filename = filename.split('media/')
    return filename[1]


def goods_img_1_path(instance, filename):
    filename = filename.split('media/')
    return filename[1]


class Goods(models.Model):
    img = models.ImageField('메인이미지', upload_to=goods_img_path)
    info_img = models.ImageField('상품 이미지', upload_to=goods_info_img_path)
    title = models.CharField('상품 명', max_length=60)
    short_desc = models.CharField('간단 설명', max_length=100)
    price = models.IntegerField('가격')
    each = models.CharField('판매 단위', max_length=64, null=True, )
    weight = models.CharField('중량/용량', max_length=64, null=True, )
    transfer = models.CharField('배송 구분', max_length=64, null=True, )
    packing = models.CharField('포장 타입', max_length=128, null=True, )
    origin = models.CharField('원산지', max_length=48, null=True, )
    allergy = models.CharField('알레르기 정보', max_length=512, null=True, )
    info = models.CharField('제품 정보', max_length=512, null=True, )
    expiration = models.CharField('유통기한', max_length=512, null=True, )

    category = models.ForeignKey(
        'goods.Category',
        on_delete=models.CASCADE,
    )

    @staticmethod
    def get_crawling():
        crawling()


class GoodsExplain(models.Model):
    img = models.ImageField('상품 설명 이미지', upload_to=goods_img_1_path)
    text_title = models.CharField(max_length=64)
    text_context = models.CharField('상품 문맥', max_length=128)
    text_description = models.CharField('설명', max_length=512)
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
        related_name='explains',
    )


class GoodsDetail(models.Model):
    detail_title = models.ForeignKey(
        'goods.GoodsDetailTitle',
        on_delete=models.CASCADE,
    )
    detail_desc = models.CharField(max_length=512)
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
        related_name='details'
    )


class GoodsDetailTitle(models.Model):
    title = models.CharField(max_length=128)


class Type(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(
        'goods.Category',
        on_delete=models.CASCADE,
    )


class Category(models.Model):
    name = models.CharField(max_length=30)


class GoodsType(models.Model):
    type = models.ForeignKey(
        'goods.Type',
        on_delete=models.CASCADE,
        related_name='types',
        related_query_name='types',
    )
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
        related_name='types',
        related_query_name='types'
    )


class DeliveryInfo(models.Model):
    pass

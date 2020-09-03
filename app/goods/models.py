from django.db import models

from goods.crawling.event import evenvt_crawling
from goods.crawling.goods import crawling
import random


def goods_img_path(instance, filename):
    if 'media/' in filename:
        filename = filename.split('media/')
        return filename[1]
    return filename


def goods_info_img_path(instance, filename):
    if 'media/' in filename:
        filename = filename.split('media/')
        return filename[1]
    return filename


def goods_img_1_path(instance, filename):
    if 'media/' in filename:
        filename = filename.split('media/')
        return filename[1]
    return filename


def delivery_img(instance, filename):
    if 'media/' in filename:
        filename = filename.split('media/')
        return filename[1]
    return filename


class Goods(models.Model):
    img = models.ImageField('메인이미지', upload_to=goods_img_path)
    info_img = models.ImageField('상품 이미지', upload_to=goods_info_img_path, null=True)
    title = models.CharField('상품 명', max_length=60)
    short_desc = models.CharField('간단 설명', max_length=100)
    price = models.IntegerField('가격')
    each = models.CharField('판매 단위', max_length=64, null=True, )
    weight = models.CharField('중량/용량', max_length=64, null=True, )
    transfer = models.CharField('배송 구분', max_length=64, null=True, )
    packing = models.CharField('포장 타입', max_length=255, null=True, )
    packing_status = models.CharField('포장 상태', max_length=48, null=True)
    origin = models.CharField('원산지', max_length=48, null=True, )
    allergy = models.CharField('알레르기 정보', max_length=512, null=True, )
    info = models.CharField('제품 정보', max_length=512, null=True, )
    expiration = models.CharField('유통기한', max_length=512, null=True, )

    category = models.ForeignKey(
        'goods.Category',
        on_delete=models.CASCADE,
        null=True,
    )
    event = models.ForeignKey(
        'event.Event',
        on_delete=models.CASCADE,
        null=True,
        related_name='goods',
    )

    sales = models.ForeignKey(
        'goods.SaleInfo',
        on_delete=models.SET_NULL,
        null=True,
        related_name='goods',
    )

    @staticmethod
    def get_crawling():
        # 상품 크롤링
        crawling()

    @staticmethod
    def get_event():
        # 이벤트 상품 크롤링
        evenvt_crawling()

    @staticmethod
    def random_discount_rate():
        pk_lst = []
        range_limit = Goods.objects.all().count()
        while True:
            val = random.randint(1, range_limit)
            if val in pk_lst:
                continue
            else:
                pk_lst.append(val)
            if len(pk_lst) == 200:
                break

        s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 = SaleInfo.objects.all()[:10]

        for index, pk in enumerate(pk_lst):
            if index < 20:
                print('5-----------------------------------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s1
                goods.save()
            elif index >= 20 and index < 40:
                print('10---------------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s2
                goods.save()
            elif index >= 40 and index < 60:
                print('15-----------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s3
                goods.save()
            elif index >= 60 and index < 80:
                print('20------------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s4
                goods.save()
            elif index >= 80 and index < 100:
                print('25-----------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s5
                goods.save()
            elif index >= 100 and index < 120:
                print('30-----------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s6
                goods.save()
            elif index >= 120 and index < 140:
                print('35-----------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s7
                goods.save()
            elif index >= 140 and index < 160:
                print('40-----------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s8
                goods.save()
            elif index >= 160 and index < 180:
                print('45-----------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s9
                goods.save()
            elif index >= 180 and index < 200:
                print('50-----------', index)
                goods = Goods.objects.get(pk=pk)
                goods.sales = s10
                goods.save()


class GoodsExplain(models.Model):
    img = models.ImageField('상품 설명 이미지', upload_to=goods_img_1_path)
    text_title = models.CharField(max_length=64)
    text_context = models.CharField('상품 문맥', max_length=255)
    text_description = models.CharField('설명', max_length=1024)
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
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Type(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(
        'goods.Category',
        on_delete=models.CASCADE,
        related_name='types'
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


class DeliveryInfoImageFile(models.Model):
    address_img = models.ImageField(upload_to='delivery_img', null=True)


class DeliveryInfoImageImageFile(models.Model):
    image = models.ImageField(
        upload_to='delivery_img',
        null=True,
    )
    info = models.ForeignKey(
        'goods.DeliveryInfoImageFile',
        on_delete=models.CASCADE,
        related_name='images'
    )


class SaleInfo(models.Model):
    discount_rate = models.IntegerField(null=True, )
    contents = models.CharField(max_length=30, null=True, )

from django.db import models

# Create your models here.
import goods
from goods.crawling import crawling


def goods_img_path(instance, filename):
    filename = filename.split('media/')
    return filename[1]


def goods_info_img_path(instance, filename):
    filename = filename.split('media/')
    return filename[1]


def goods_img_1_path(instance, filename):
    filename = filename.split('media/')
    return filename[1]


class Goods(models.Model):
    # 디테일 상위
    img = models.ImageField('메인이미지', upload_to=goods_img_path)
    info_img = models.ImageField('상품 이미지', upload_to=goods_info_img_path)
    title = models.CharField('상품 명', max_length=30)
    short_desc = models.CharField('간단 설명', max_length=50)
    price = models.IntegerField('가격')
    each = models.CharField('판매 단위', max_length=24, null=True, )
    weight = models.CharField('중량/용량', max_length=24, null=True, )
    transfer = models.CharField('배송 구분', max_length=24, null=True, )
    packing = models.CharField('포장 타입', max_length=64, null=True, )
    origin = models.CharField('원산지', max_length=48, null=True, )
    allergy = models.CharField('알레르기 정보', max_length=126, null=True, )
    info = models.CharField('제품 정보', max_length=126, null=True, )
    expiration = models.CharField('유통기한', max_length=64, null=True, )

    # 디테일 중반
    img_1 = models.ImageField('디테일 이미지1', upload_to=goods_img_1_path)
    text_1_title = models.CharField('첫 텍스트', max_length=64)
    text_1_context = models.CharField('첫 문맥', max_length=128)
    text_1_description = models.CharField('설명', max_length=512)

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
    )

    @staticmethod
    def get_crawling():
        crawling()


class GoodsDetail(models.Model):
    goods = models.OneToOneField(Goods, on_delete=models.CASCADE)
    var_1_title = models.CharField(max_length=64, null=True, blank=True)
    var_1_desc = models.CharField(max_length=64, null=True, blank=True)
    var_2_title = models.CharField(max_length=64, null=True, blank=True)
    var_2_desc = models.CharField(max_length=64, null=True, blank=True)
    var_3_title = models.CharField(max_length=64, null=True, blank=True)
    var_3_desc = models.CharField(max_length=64, null=True, blank=True)
    var_4_title = models.CharField(max_length=64, null=True, blank=True)
    var_4_desc = models.CharField(max_length=64, null=True, blank=True)
    var_5_title = models.CharField(max_length=64, null=True, blank=True)
    var_5_desc = models.CharField(max_length=64, null=True, blank=True)
    var_6_title = models.CharField(max_length=64, null=True, blank=True)
    var_6_desc = models.CharField(max_length=64, null=True, blank=True)
    var_7_title = models.CharField(max_length=64, null=True, blank=True)
    var_7_desc = models.CharField(max_length=64, null=True, blank=True)
    var_8_title = models.CharField(max_length=64, null=True, blank=True)
    var_8_desc = models.CharField(max_length=64, null=True, blank=True)
    var_9_title = models.CharField(max_length=64, null=True, blank=True)
    var_9_desc = models.CharField(max_length=64, null=True, blank=True)
    var_10_title = models.CharField(max_length=64, null=True, blank=True)
    var_10_desc = models.CharField(max_length=64, null=True, blank=True)


class Type(models.Model):
    name = models.CharField(max_length=30)


class Category(models.Model):
    name = models.CharField(max_length=30)


class GoodsType(models.Model):
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
    )
    goods = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
    )

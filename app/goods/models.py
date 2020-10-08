from django.db import models

from goods.crawling.event import evenvt_crawling
from goods.crawling.goods import crawling
import secrets


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


def category_img(instance, filename):
    import datetime
    data = filename + datetime.datetime.now().strftime('%y/%m/%d')
    return data


class Goods(models.Model):
    img = models.ImageField(help_text='메인이미지', upload_to=goods_img_path)
    info_img = models.ImageField(help_text='상품 이미지', upload_to=goods_info_img_path, null=True)
    title = models.CharField(help_text='상품 명', max_length=60)
    short_desc = models.CharField(help_text='간단 설명', max_length=100)
    price = models.PositiveIntegerField(help_text='가격', db_index=True)
    each = models.CharField(help_text='판매 단위', max_length=64, null=True, )
    weight = models.CharField(help_text='중량/용량', max_length=64, null=True, )
    transfer = models.CharField(help_text='배송 구분', max_length=64, null=True, )
    packing = models.CharField(help_text='포장 타입', max_length=255, null=True, )
    packing_status = models.CharField(help_text='포장 상태', max_length=48, null=True)
    origin = models.CharField(help_text='원산지', max_length=48, null=True, )
    allergy = models.CharField(help_text='알레르기 정보', max_length=512, null=True, )
    info = models.CharField(help_text='제품 정보', max_length=512, null=True, )
    expiration = models.CharField(help_text='유통기한', max_length=512, null=True, )
    sales_count = models.PositiveSmallIntegerField(help_text='판매량', default=0, blank=True, db_index=True)

    event = models.ForeignKey(
        'event.Event',
        on_delete=models.CASCADE,
        null=True,
        related_name='goods',
        help_text='홈-이벤트'
    )

    sales = models.ForeignKey(
        'goods.SaleInfo',
        on_delete=models.SET_NULL,
        null=True,
        related_name='goods',
        help_text='세일정보',
    )

    def save(self, *args, **kwargs):
        created = self.pk
        if created is None:
            super().save(*args, **kwargs)
            Stock.objects.create(goods=self)
        else:
            super().save(*args, **kwargs)

    @property
    def discount_price(self):
        try:
            if type(self.sales.discount_rate) is int:
                price = (100 - self.sales.discount_rate) * 0.01 * self.price
                return int(price)
            return None

        except AttributeError:
            return None

    @staticmethod
    def get_crawling():
        # 상품 크롤링
        crawling()

    @staticmethod
    def get_event():
        # 이벤트 상품 크롤링
        evenvt_crawling()

    @staticmethod
    def set_goods_packing_status():
        # 상품 카트에 담길 시 포장 상태 표기 동작 함수
        for i in Goods.objects.all():
            try:
                if '상온' in i.packing:
                    i.packing_status = '상온'
                elif '냉장' in i.packing:
                    i.packing_status = '냉장'
                elif '냉동' in i.packing:
                    i.packing_status = '냉동'
                i.save()
            except TypeError:
                continue

    @staticmethod
    def random_discount_rate():
        id_lst = []
        range_limit = Goods.objects.all().count()
        while True:
            val = secrets.randbelow(range_limit)
            if val in id_lst:
                continue
            elif val == 0:
                continue
            else:
                id_lst.append(val)
            if len(id_lst) == 200:
                break

        s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 = SaleInfo.objects.all()[:10]

        for index, id in enumerate(id_lst):
            if index < 20:
                print('5-----------------------------------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s1
                goods.save()
            elif index >= 20 and index < 40:
                print('10---------------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s2
                goods.save()
            elif index >= 40 and index < 60:
                print('15-----------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s3
                goods.save()
            elif index >= 60 and index < 80:
                print('20------------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s4
                goods.save()
            elif index >= 80 and index < 100:
                print('25-----------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s5
                goods.save()
            elif index >= 100 and index < 120:
                print('30-----------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s6
                goods.save()
            elif index >= 120 and index < 140:
                print('35-----------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s7
                goods.save()
            elif index >= 140 and index < 160:
                print('40-----------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s8
                goods.save()
            elif index >= 160 and index < 180:
                print('45-----------', index)
                goods = Goods.objects.get(id=id)
                goods.sales = s9
                goods.save()
            elif index >= 180 and index < 200:
                print('50-----------', index)
                goods = Goods.objects.get(id=id)
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
    category_img = models.ImageField(upload_to=category_img, null=True)


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


class SaleInfo(models.Model):
    discount_rate = models.PositiveSmallIntegerField(null=True, db_index=True)
    contents = models.CharField(max_length=30, null=True, )


class Tag(models.Model):
    name = models.CharField(max_length=36)


class Tagging(models.Model):
    tag = models.ForeignKey(
        'goods.Tag',
        on_delete=models.CASCADE,
        related_name='tagging'
    )
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
        related_name='tagging'
    )


class Stock(models.Model):
    count = models.PositiveSmallIntegerField(help_text='상품 재고량', default=0, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, help_text='입고 날짜')
    goods = models.OneToOneField('goods.Goods', on_delete=models.CASCADE, )

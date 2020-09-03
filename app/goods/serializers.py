from action_serializer import ModelActionSerializer, serializers
from rest_framework.serializers import ModelSerializer
from goods.models import Category, GoodsExplain, GoodsDetailTitle, GoodsDetail, Goods, DeliveryInfoImageFile, \
    DeliveryInfoImageImageFile, Type, SaleInfo


# 상품 세일 정보
class SalesInfoSerializers(ModelSerializer):
    class Meta:
        model = SaleInfo
        fields = ('discount_rate', 'contents')


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class GoodsExplainSerializers(ModelSerializer):
    class Meta:
        model = GoodsExplain
        fields = ('img', 'text_title', 'text_context', 'text_description')


class GoodsDetailTitleSerializers(ModelSerializer):
    class Meta:
        model = GoodsDetailTitle
        fields = ('title',)


class GoodsDetailSerializers(ModelSerializer):
    detail_title = GoodsDetailTitleSerializers()

    class Meta:
        model = GoodsDetail
        fields = ('detail_title', 'detail_desc')


class MinimumGoodsSerializers(ModelSerializer):
    class Meta:
        model = Goods
        fields = ('id', 'title', 'img', 'price', 'packing_status')


class GoodsSaleSerializers(ModelSerializer):
    sales = SalesInfoSerializers()

    class Meta:
        model = Goods
        fields = (
            'id',
            'title',
            'short_desc',
            'price',
            'img',
            'sales'
        )


class GoodsSerializers(ModelActionSerializer):
    explains = GoodsExplainSerializers(many=True)
    details = GoodsDetailSerializers(many=True, )
    sales = SalesInfoSerializers()

    class Meta:
        model = Goods
        fields = ('id',
                  'img',
                  'info_img',
                  'title',
                  'short_desc',
                  'price',
                  'each',
                  'weight',
                  'transfer',
                  'packing',
                  'origin',
                  'allergy',
                  'info',
                  'expiration',
                  'explains',
                  'details',
                  )
        action_fields = {
            'list': {'fields': ('id', 'title', 'short_desc', 'price', 'img', 'sales')},
        }


class DeliveryInfoImageSerializers(ModelSerializer):
    class Meta:
        model = DeliveryInfoImageFile
        fields = (
            'image',
        )


class DeliveryInfoSerializers(ModelSerializer):
    images = DeliveryInfoImageSerializers(many=True)

    class Meta:
        model = DeliveryInfoImageImageFile
        fields = ('address_img', 'images')


class TypeSerializers(ModelSerializer):
    class Meta:
        model = Type
        fields = ('name',)


class CategoriesSerializers(ModelSerializer):
    types = TypeSerializers(many=True, )

    class Meta:
        model = Category
        fields = ('name', 'types')

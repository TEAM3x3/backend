from action_serializer import ModelActionSerializer, serializers
from rest_framework.serializers import ModelSerializer

from carts.models import CartItem
from goods.models import Category, GoodsExplain, GoodsDetailTitle, GoodsDetail, Goods, DeliveryInfoImage, DeliveryInfo, \
    Type


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


class GoodsSerializers(ModelActionSerializer):
    explains = GoodsExplainSerializers(many=True)
    details = GoodsDetailSerializers(many=True, )

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
            'list': {'fields': ('id', 'title', 'short_desc', 'price', 'img',)}
        }


class DeliveryInfoImageSerializers(ModelSerializer):
    class Meta:
        model = DeliveryInfoImage
        fields = (
            'image',
        )


class DeliveryInfoSerializers(ModelSerializer):
    images = DeliveryInfoImageSerializers(many=True)

    class Meta:
        model = DeliveryInfo
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

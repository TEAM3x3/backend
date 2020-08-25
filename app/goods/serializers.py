from action_serializer import ModelActionSerializer
from rest_framework.serializers import ModelSerializer

from goods.models import Goods, GoodsExplain, GoodsDetail, Category


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class GoodsExplainSerializers(ModelSerializer):
    class Meta:
        model = GoodsExplain
        fields = ('img', 'text_title', 'text_context', 'text_description')


class GoodsDetailSerializers(ModelSerializer):
    class Meta:
        model = GoodsDetail
        fields = ('detail_title', 'detail_desc')


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

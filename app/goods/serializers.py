from action_serializer import ModelActionSerializer, serializers
from rest_framework.serializers import ModelSerializer
from goods.models import Category, GoodsExplain, GoodsDetailTitle, GoodsDetail, Goods, Type, SaleInfo, Tag, Tagging


# 상품 세일 정보
class SalesInfoSerializers(ModelSerializer):
    class Meta:
        model = SaleInfo
        fields = ('discount_rate', 'contents')


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'category_img')


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


class TagSerializers(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class TaggingSerializers(ModelSerializer):
    tag = TagSerializers()

    class Meta:
        model = Tagging
        fields = ('tag',)


class GoodsSaleSerializers(ModelSerializer):
    sales = SalesInfoSerializers()
    tagging = TaggingSerializers(many=True)
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = (
            'id',
            'title',
            'short_desc',
            'packing_status',
            'price',
            'img',
            'sales',
            'tagging',
            'discount_price',
        )

    def get_discount_price(self, obj):
        try:
            if type(obj.sales.discount_rate) is int:
                value = ((100 - obj.sales.discount_rate) * 0.01) * obj.price
                return int(value)
            return None
        except AttributeError:
            return None


class GoodsSerializers(ModelActionSerializer):
    explains = GoodsExplainSerializers(many=True)
    details = GoodsDetailSerializers(many=True)
    discount_price = serializers.SerializerMethodField()
    sales = SalesInfoSerializers()

    class Meta:
        model = Goods
        fields = ('id',
                  'img',
                  'info_img',
                  'title',
                  'short_desc',
                  'price',
                  'sales',
                  'discount_price',
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
            'list': {'fields': ('id', 'title', 'short_desc', 'price', 'img',)},
            'main_page_recommend': {'fields': ('id', 'title',)},
        }

    def get_discount_price(self, obj):
        return obj.discount_price


class TypeSerializers(ModelSerializer):
    class Meta:
        model = Type
        fields = ('name',)


class CategoriesSerializers(ModelSerializer):
    types = TypeSerializers(many=True, )

    class Meta:
        model = Category
        fields = ('name', 'category_img', 'types',)

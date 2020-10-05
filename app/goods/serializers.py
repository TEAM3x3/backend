from action_serializer import ModelActionSerializer, serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from goods.models import Category, GoodsExplain, GoodsDetailTitle, GoodsDetail, Goods, Type, SaleInfo, Tag, Tagging, \
    Stock

# 상품 세일 정보
from order.models import OrderReview

User = get_user_model()


class SalesInfoSerializers(ModelSerializer):
    class Meta:
        model = SaleInfo
        fields = ('discount_rate', 'contents')


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'category_img')


class UserOrderSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class OrderReviewSerializers(ModelSerializer):
    user = UserOrderSerializers()

    class Meta:
        model = OrderReview
        fields = ('id', 'title', 'content', 'user')


class GoodsReviewSerializers(ModelSerializer):
    reviews = OrderReviewSerializers(many=True)

    class Meta:
        model = Goods
        fields = ('id', 'title', 'price', 'info_img', 'reviews')


class CategoryGoodsSerializers(ModelSerializer):
    goods = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'goods')

    def get_goods(self, obj):
        import random
        # md 추천 상품 숫자.
        home_md_recommend_goods_limit = 6
        qs = Goods.objects.filter(types__type__category=obj)
        max_id = 0
        min_id = 5000
        for obj in qs:
            if obj.id < min_id:
                min_id = obj.id
            if obj.id > max_id:
                max_id = obj.id
        int_list = []
        while True:
            # 1 , 716
            rand_int = random.randint(min_id, max_id)
            if rand_int in int_list:
                continue
            else:
                int_list.append(rand_int)
            if len(int_list) == home_md_recommend_goods_limit:
                break
        qs = Goods.objects.filter(pk__in=int_list)
        serializers = GoodsSaleSerializers(qs, many=True)
        return serializers.data


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


class StockSerializers(ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'count', 'updated_at')


class GoodsSaleSerializers(ModelSerializer):
    sales = SalesInfoSerializers()
    tagging = TaggingSerializers(many=True)
    discount_price = serializers.SerializerMethodField()
    stock = StockSerializers()

    class Meta:
        model = Goods
        fields = (
            'id',
            'title',
            'short_desc',
            'packing_status',
            'transfer',
            'price',
            'img',
            'sales',
            'tagging',
            'discount_price',
            'sales_count',
            'stock'
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
        examples = {
            "id": 1,
            "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKF365%5D%20%ED%96%87%20%EA%B0%90%EC%9E%90%201kg/KF365_%ED%96%87_%EA%B0%90%EC%9E%90_1kg_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T162027Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=1527c8c97cd28360d770e076f214050bd526db642764ca7b330e3a380487df10",
            "info_img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKF365%5D%20%ED%96%87%20%EA%B0%90%EC%9E%90%201kg/KF365_%ED%96%87_%EA%B0%90%EC%9E%90_1kg_info_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T162027Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=7a3945e825f00b4ceda952b65585fd0e74739a9a5f85450ff19338c7d26a6394",
            "title": "[KF365] 햇 감자 1kg",
            "short_desc": "믿고 먹을 수 있는 상품을 합리적인 가격에, KF365",
            "price": 2380,
            "sales": 'null',
            "discount_price": 'null',
            "each": "1봉",
            "weight": "1kg",
            "transfer": "샛별배송/택배배송",
            "packing": "상온/종이포장\n택배배송은 에코포장이 스티로폼으로 대체됩니다.",
            "origin": "국내산",
            "allergy": 'null',
            "info": "식품 특성상 중량은 3% 내외의 차이가 발생할 수 있습니다.\n시세에 따라 가격이 변동 될 수 있습니다.\n햇빛을 피해 보관해 주시기 바라며 햇빛을 받아 껍질이나 내부가 초록색으로 변한 경우 섭취하지 마시기 바랍니다.\n'하우스 햇감자'로 배송 드립니다.",
            "expiration": 'null',
            "explains": [
                {
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKF365%5D%20%ED%96%87%20%EA%B0%90%EC%9E%90%201kg/KF365_%ED%96%87_%EA%B0%90%EC%9E%90_1kg_image_one.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T162027Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3b1285ad2b67f4ba2bfe9718c5aa433f4bc9ffb08f30e97066b9e1d0e2f12941",
                    "text_title": "포슬포슬하고 고소한 맛",
                    "text_context": "감자 1kg ",
                    "text_description": "간단히 쪄 먹기도 좋고, 다양한 요리와 함께 곁들여 먹기도 좋은 감자는 우리 식탁에 빼놓을 수 없는 식재료지요. 탄수화물은 물론이고 단백질, 비타민C까지 풍부해 마치 곡류와 채소를 동시에 먹은 것과 같은 효과를 줍니다. 컬리는 그때그때 유명산지 감자를 가락시장에서 수급하여 보내드립니다. 포슬포슬한 식감에 고소하고 은은한 단맛이 나 볶음, 구이, 튀김 등 다양하게 요리해서 먹을 수 있어요. 매일 식탁에 올려도 질리지 않는 감자를 컬리에서 간편하게 만나보세요."
                }
            ],
            "details": [
                {
                    "detail_title": {
                        "title": "포장단위별 용량(중량), 수량, 크기"
                    },
                    "detail_desc": "상품설명 및 상품이미지 참조"
                },
                {
                    "detail_title": {
                        "title": "관련법상 표시사항"
                    },
                    "detail_desc": "농산물 - 농수산물품질관리법상 유전자변형농산물 표시, 지리적 표시\n축산물 - 축산법에 따른 등급 표시, 쇠고기의 경우 이력관리에 따른 표시 유무\n수산물 - 농수산물품질관리법상 유전자변형수산물 표시, 지리적 표시\n수입식품에 해당하는 경우 “식품위생법에 따른 수입신고를 필함”의 문구"
                },
                {
                    "detail_title": {
                        "title": "생산자, 수입품의 경우 수입자를 함께 표기"
                    },
                    "detail_desc": "제품 별도 라벨 표기 참조"
                },
                {
                    "detail_title": {
                        "title": "상품구성"
                    },
                    "detail_desc": "상품설명 및 상품이미지 참조"
                },
                {
                    "detail_title": {
                        "title": "농수산물의 원산지 표시에 관한 법률에 따른 원산지"
                    },
                    "detail_desc": "상품설명 및 상품이미지 참조"
                },
                {
                    "detail_title": {
                        "title": "보관방법 또는 취급방법"
                    },
                    "detail_desc": "냉장보관"
                },
                {
                    "detail_title": {
                        "title": "제조연월일(포장일 또는 생산연도), 유통기한 또는 품질유지기한"
                    },
                    "detail_desc": "제품 별도 라벨 표기 참조"
                },
                {
                    "detail_title": {
                        "title": "소비자상담 관련 전화번호"
                    },
                    "detail_desc": "마켓컬리 고객행복센터(1644-1107)"
                }
            ]
        }
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
        examples = [
            {
                "name": "채소",
                "category_img": "https://pbs-13-s3.s3.amazonaws.com/category_img/icon_veggies_active_pc2x.1586324570.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T195332Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=6f32586de61e684046b11336bce7759268e622812028b6b7b66315c1e203421e",
                "types": [
                    {
                        "name": "기본채소"
                    },
                    {
                        "name": "쌈·샐러드·간편채소"
                    },
                    {
                        "name": "브로콜리·특수채소"
                    },
                    {
                        "name": "콩나물·버섯류"
                    },
                    {
                        "name": "시금치·부추·나물"
                    },
                    {
                        "name": "양파·마늘·생강·파"
                    },
                    {
                        "name": "파프리카·피망·고추"
                    }
                ]
            }
        ]

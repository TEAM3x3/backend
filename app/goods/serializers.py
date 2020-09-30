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
        examples = {
            "id": 2,
            "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%ED%95%9C%EB%81%BC%20%EB%8B%B9%EA%B7%BC%201%EA%B0%9C/%ED%95%9C%EB%81%BC_%EB%8B%B9%EA%B7%BC_1%EA%B0%9C_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200916%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200916T073320Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e812d91c6cf3427766138ad5efb58e54b18bcd20d63ebb614f7a069f5ea9c266",
            "info_img": "https://pbs-13-s3.s3.amazonaws.com/goods/%ED%95%9C%EB%81%BC%20%EB%8B%B9%EA%B7%BC%201%EA%B0%9C/%ED%95%9C%EB%81%BC_%EB%8B%B9%EA%B7%BC_1%EA%B0%9C_info_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200916%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200916T073320Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=1ac806d619ba6e97edaecfb1cc7208fc0be92d7e826fb7a5bbd49762060e408d",
            "title": "한끼 당근 1개",
            "short_desc": "딱 하나만 필요할 때 한끼 당근",
            "price": 1000,
            "sales": {
                "discount_rate": 30,
                "contents": 'null'
            },
            "discount_price": 700,
            "each": "1봉",
            "weight": "1개",
            "transfer": "샛별배송/택배배송",
            "packing": "냉장/종이포장\n택배배송은 에코포장이 스티로폼으로 대체됩니다.",
            "origin": "국산",
            "allergy": 'null',
            "info": 'null',
            "expiration": "농산물로 별도의 유통기한은 없으나 가급적 빠르게 드시기 바랍니다.",
            "explains": [
                {
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%ED%95%9C%EB%81%BC%20%EB%8B%B9%EA%B7%BC%201%EA%B0%9C/%ED%95%9C%EB%81%BC_%EB%8B%B9%EA%B7%BC_1%EA%B0%9C_image_one.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200916%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200916T073320Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=07b69de64c3366518f858465338d7aeb045b9382ba5be216bcb44897b0f959b9",
                    "text_title": "베타카로틴이 풍부한 주홍빛 채소",
                    "text_context": "한끼 당근 ",
                    "text_description": "아삭아삭한 식감과 은은한 단맛을 지닌 당근. 김밥이나 계란말이처럼 우리 일상을 든든하게 채워주는 음식에 꼭 들어가는 반가운 채소인데요. 주홍빛 당근 하나만 더해줘도 요리의 색감이 화사하게 피어나지요. 요리에 자주 사용하는 필수 재료지만, 한 번에 많이 구비해두면 보관하기도 힘들고 쉽게 무르곤 해요. 그래서 컬리는 당근을 딱 한끼 깔끔하게 즐길 수 있는 분량만큼 담아 보내드립니다. 번거롭게 손질할 일도 없고 남은 재료를 어떻게 처리할지 걱정할 필요도 없지요. 끼니마다 신선한 채소로 다채로운 요리를 완성해보세요."
                }
            ],
            "details": [
                {
                    "detail_title": {
                        "title": "포장단위별 용량(중량), 수량, 크기"
                    },
                    "detail_desc": "1개"
                },
                {
                    "detail_title": {
                        "title": "관련법상 표시사항"
                    },
                    "detail_desc": "해당사항 없음"
                },
                {
                    "detail_title": {
                        "title": "생산자, 수입품의 경우 수입자를 함께 표기"
                    },
                    "detail_desc": "농업회사법인 (주)록야"
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
                    "detail_desc": "국산"
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
                    "detail_desc": "농산물로 유통기한 없음"
                },
                {
                    "detail_title": {
                        "title": "소비자상담 관련 전화번호"
                    },
                    "detail_desc": "마켓컬리 고객행복센터(1644-1107)"
                }
            ]
        }

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

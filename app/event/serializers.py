from action_serializer import ModelActionSerializer
from rest_framework.serializers import ModelSerializer

from .models import Event, MainEvent, MainEventType, GoodsEventType
from goods.serializers import GoodsSaleSerializers


class EventImageSquareSerializers(ModelSerializer):
    goods = GoodsSaleSerializers(many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'square_image', 'goods')


class EventSerializers(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'image')


class EventRetrieveSerializers(ModelSerializer):
    goods = GoodsSaleSerializers(many=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'goods')
        examples = {
            "id": 1,
            "title": "[모음전] 해물육수",
            "goods": [
                {
                    "id": 1217,
                    "title": "[바다원] 대관령 북어채 100g",
                    "short_desc": "반찬 걱정 덜어주는 구수한 감칠맛",
                    "packing_status": "냉장",
                    "transfer": "샛별배송/택배배송",
                    "price": 6715,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EB%8C%80%EA%B4%80%EB%A0%B9%20%EB%B6%81%EC%96%B4%EC%B1%84%20100g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EB%8C%80%EA%B4%80%EB%A0%B9_%EB%B6%81%EC%96%B4%EC%B1%84_100g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T205446Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=acb4c60f632502ec5858911f247d6473666647b11d561b7e1880b7e4d462b1c4",
                    "sales": {
                        "discount_rate": 'null',
                        "contents": "1+1"
                    },
                    "tagging": [],
                    "discount_price": 'null'
                },
                {
                    "id": 1218,
                    "title": "[바다원] 야채 국물용팩 90g",
                    "short_desc": "시원하고 깔끔한 맛",
                    "packing_status": "냉장",
                    "transfer": "샛별배송/택배배송",
                    "price": 5015,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EC%95%BC%EC%B1%84%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9%2090g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EC%95%BC%EC%B1%84_%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9_90g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T205447Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=2e4a6f8a71e9fd070a08a07fa4d6a9714d2180031a72af4d50aca0d1ce81370d",
                    "sales": {
                        "discount_rate": 5,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 4764
                },
                {
                    "id": 1219,
                    "title": "[바다원] 꽃게 국물용팩 90g",
                    "short_desc": "손쉽게 더하는 꽃게의 감칠맛",
                    "packing_status": "냉장",
                    "transfer": "샛별배송/택배배송",
                    "price": 5015,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EA%BD%83%EA%B2%8C%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9%2090g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EA%BD%83%EA%B2%8C_%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9_90g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T205447Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=0d36df5eb46a62943208f7169e461ea985bec662f3bd04852ae2e0c57a4b372a",
                    "sales": {
                        "discount_rate": 10,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 4513
                },
            ]
        }


class GoodsEventTypeSerializers(ModelSerializer):
    goods = GoodsSaleSerializers()

    class Meta:
        model = GoodsEventType
        fields = ('goods',)


class MainEventTypeSerializers(ModelSerializer):
    mainEvent = GoodsEventTypeSerializers(many=True)

    class Meta:
        model = MainEventType
        fields = ('id', 'name', 'mainEvent')


class MainEventSerializers(ModelActionSerializer):
    class Meta:
        model = MainEvent
        fields = ('id', 'title', 'image',)


class MainEventRetrieveSerializers(ModelSerializer):
    event = MainEventTypeSerializers(many=True)

    class Meta:
        model = MainEvent
        fields = ('id', 'title', 'detail_image', 'event')
        examples = {
            "id": 1,
            "title": "매콤달콤 우리집 식탁",
            "detail_image": 'null',
            "event": [
                {
                    "id": 1,
                    "name": "매운맛",
                    "mainEvent": [
                        {
                            "goods": {
                                "id": 1257,
                                "title": "[Kurly X 팔당] 불비빔냉면 2인분",
                                "short_desc": "홍두깨살을 얹어 더 맛있게 매운",
                                "packing_status": "냉동",
                                "transfer": "샛별배송/택배배송",
                                "price": 9180,
                                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKurly%20X%20%ED%8C%94%EB%8B%B9%5D%20%EB%B6%88%EB%B9%84%EB%B9%94%EB%83%89%EB%A9%B4%202%EC%9D%B8%EB%B6%84/Kurly_X_%ED%8C%94%EB%8B%B9_%EB%B6%88%EB%B9%84%EB%B9%94%EB%83%89%EB%A9%B4_2%EC%9D%B8%EB%B6%84_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T205612Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c2d4fc35967b9e5551f957342ff7384950096a3a2b301d1b00f5a0a8908eb6df",
                                "sales": {
                                    "discount_rate": 15,
                                    "contents": 'null'
                                },
                                "tagging": [],
                                "discount_price": 7803
                            }
                        },
                        {
                            "goods": {
                                "id": 1258,
                                "title": "[미트클레버] 춘천 닭갈비",
                                "short_desc": "집에서 즐기는 춘천의 맛!",
                                "packing_status": 'null',
                                "transfer": 'null',
                                "price": 10620,
                                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%AF%B8%ED%8A%B8%ED%81%B4%EB%A0%88%EB%B2%84%5D%20%EC%B6%98%EC%B2%9C%20%EB%8B%AD%EA%B0%88%EB%B9%84/%EB%AF%B8%ED%8A%B8%ED%81%B4%EB%A0%88%EB%B2%84_%EC%B6%98%EC%B2%9C_%EB%8B%AD%EA%B0%88%EB%B9%84_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T205612Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=292692dd8b23be75b40b0d17984126fceadbcd490f70e447d2d837b12635cf1d",
                                "sales": {
                                    "discount_rate": 10,
                                    "contents": 'null'
                                },
                                "tagging": [],
                                "discount_price": 9558
                            }
                        }
                    ]
                }
            ]
        }

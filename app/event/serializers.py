from action_serializer import ModelActionSerializer
from rest_framework.serializers import ModelSerializer

from .models import Event, MainEvent, MainEventType, GoodsEventType
from goods.serializers import GoodsSaleSerializers


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
                    "price": 6715,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EB%8C%80%EA%B4%80%EB%A0%B9%20%EB%B6%81%EC%96%B4%EC%B1%84%20100g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EB%8C%80%EA%B4%80%EB%A0%B9_%EB%B6%81%EC%96%B4%EC%B1%84_100g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=89113a5a805a62d88562ad78ee74e0625dbe165d940c5630f2418fff32a41ce2",
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
                    "price": 5015,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EC%95%BC%EC%B1%84%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9%2090g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EC%95%BC%EC%B1%84_%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9_90g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=f2b956befcb6603c359858f75523ef35a21db6364d944c01eebe07bfce484aad",
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
                    "price": 5015,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EA%BD%83%EA%B2%8C%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9%2090g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EA%BD%83%EA%B2%8C_%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9_90g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=0a1fdbd6223af34ac8422863ba049d4e7f6aa802cfedc6de332a41533ae07707",
                    "sales": {
                        "discount_rate": 10,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 4513
                },
                {
                    "id": 1220,
                    "title": "[바다원] 디포리 국물용팩 90g",
                    "short_desc": "한 팩에 담긴 깊은 감칠맛",
                    "packing_status": "냉장",
                    "price": 5015,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EB%94%94%ED%8F%AC%EB%A6%AC%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9%2090g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EB%94%94%ED%8F%AC%EB%A6%AC_%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9_90g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=8e6aa56b401f4396ec164849e4ee9bb727c82a70b716bbc9dbcd79608c369d01",
                    "sales": {
                        "discount_rate": 10,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 4513
                },
                {
                    "id": 1221,
                    "title": "[바다원] 멸치 국물용팩 90g",
                    "short_desc": "하나로 끝내는 멸치 육수",
                    "packing_status": "냉장",
                    "price": 4675,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EB%A9%B8%EC%B9%98%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9%2090g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EB%A9%B8%EC%B9%98_%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9_90g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b268ead2d32e2d46c8a97442a9e71c6473ace8331e404e7891932ecef094762b",
                    "sales": {
                        "discount_rate": 30,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 3272
                },
                {
                    "id": 1222,
                    "title": "[바다원] 훈연멸치 국물용팩 90g",
                    "short_desc": "간단하게 만드는 구수한 국물",
                    "packing_status": "냉장",
                    "price": 5695,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%ED%9B%88%EC%97%B0%EB%A9%B8%EC%B9%98%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9%2090g/%EB%B0%94%EB%8B%A4%EC%9B%90_%ED%9B%88%EC%97%B0%EB%A9%B8%EC%B9%98_%EA%B5%AD%EB%AC%BC%EC%9A%A9%ED%8C%A9_90g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c99ca7c54f5504b9b319dc2c10097012661b335e919885c26db3c9a2a44078e7",
                    "sales": 'null',
                    "tagging": [
                        {
                            "tag": {
                                "name": "한정수량"
                            }
                        }
                    ],
                    "discount_price": 'null'
                },
                {
                    "id": 1223,
                    "title": "[우주] 훈연디포리 300g(냉동)",
                    "short_desc": "깊고 시원한 국물맛을 위한",
                    "packing_status": "냉동",
                    "price": 13175,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EC%9A%B0%EC%A3%BC%5D%20%ED%9B%88%EC%97%B0%EB%94%94%ED%8F%AC%EB%A6%AC%20300g%28%EB%83%89%EB%8F%99%29/%EC%9A%B0%EC%A3%BC_%ED%9B%88%EC%97%B0%EB%94%94%ED%8F%AC%EB%A6%AC_300g%EB%83%89%EB%8F%99_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=7eb8e6172a6d2cf96d5d86e6225c2f6811d43dcb2ac74178e6f03bcfe472682d",
                    "sales": 'null',
                    "tagging": [],
                    "discount_price": 'null'
                },
                {
                    "id": 1224,
                    "title": "[바다원] 남해안 국물용멸치 180g",
                    "short_desc": "시원한 국물 맛의 비결",
                    "packing_status": "냉장",
                    "price": 7110,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EB%82%A8%ED%95%B4%EC%95%88%20%EA%B5%AD%EB%AC%BC%EC%9A%A9%EB%A9%B8%EC%B9%98%20180g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EB%82%A8%ED%95%B4%EC%95%88_%EA%B5%AD%EB%AC%BC%EC%9A%A9%EB%A9%B8%EC%B9%98_180g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=ffd01a607545f4c9f90f9b5ef660b15c386367ef925408a97e0740aea46125bb",
                    "sales": {
                        "discount_rate": 'null',
                        "contents": "1+1"
                    },
                    "tagging": [],
                    "discount_price": 'null'
                },
                {
                    "id": 1225,
                    "title": "[해강물산] 수산물 이력제 멸치 2종",
                    "short_desc": "믿고 챙기는 매일 멸치",
                    "packing_status": "냉장",
                    "price": 11000,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%ED%95%B4%EA%B0%95%EB%AC%BC%EC%82%B0%5D%20%EC%88%98%EC%82%B0%EB%AC%BC%20%EC%9D%B4%EB%A0%A5%EC%A0%9C%20%EB%A9%B8%EC%B9%98%202%EC%A2%85/%ED%95%B4%EA%B0%95%EB%AC%BC%EC%82%B0_%EC%88%98%EC%82%B0%EB%AC%BC_%EC%9D%B4%EB%A0%A5%EC%A0%9C_%EB%A9%B8%EC%B9%98_2%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c17fe1b65137aef3517cf648034d69b1f528e1cf30080e433f0d7966725efcc6",
                    "sales": {
                        "discount_rate": 50,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 5500
                },
                {
                    "id": 1226,
                    "title": "국물용 황태머리 2종 (냉장)",
                    "short_desc": "깊고 구수한 국물을 만드는 국물용 황태머리",
                    "packing_status": "냉장",
                    "price": 4500,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EA%B5%AD%EB%AC%BC%EC%9A%A9%20%ED%99%A9%ED%83%9C%EB%A8%B8%EB%A6%AC%202%EC%A2%85%20%28%EB%83%89%EC%9E%A5%29/%EA%B5%AD%EB%AC%BC%EC%9A%A9_%ED%99%A9%ED%83%9C%EB%A8%B8%EB%A6%AC_2%EC%A2%85_%EB%83%89%EC%9E%A5_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T200942Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c5edf6fa378f2a4cc21969021abc1c8870a5f792b94c4a21aae1387a4707c400",
                    "sales": {
                        "discount_rate": 20,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 3600
                }
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
                                "price": 9180,
                                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKurly%20X%20%ED%8C%94%EB%8B%B9%5D%20%EB%B6%88%EB%B9%84%EB%B9%94%EB%83%89%EB%A9%B4%202%EC%9D%B8%EB%B6%84/Kurly_X_%ED%8C%94%EB%8B%B9_%EB%B6%88%EB%B9%84%EB%B9%94%EB%83%89%EB%A9%B4_2%EC%9D%B8%EB%B6%84_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202611Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=a2dd45d994f479ad30904743b80641e7bba451c37c6219cbb9a8bc997e2fb482",
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
                                "price": 10620,
                                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%AF%B8%ED%8A%B8%ED%81%B4%EB%A0%88%EB%B2%84%5D%20%EC%B6%98%EC%B2%9C%20%EB%8B%AD%EA%B0%88%EB%B9%84/%EB%AF%B8%ED%8A%B8%ED%81%B4%EB%A0%88%EB%B2%84_%EC%B6%98%EC%B2%9C_%EB%8B%AD%EA%B0%88%EB%B9%84_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202611Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=faf48efee1de6755de78ea557a1b157748321d5eeaf5baf655bc10f0e9697ae9",
                                "sales": {
                                    "discount_rate": 10,
                                    "contents": 'null'
                                },
                                "tagging": [],
                                "discount_price": 9558
                            }
                        },
                    ]

                }
            ]
        }

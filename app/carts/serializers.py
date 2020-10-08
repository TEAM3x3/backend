from action_serializer import ModelActionSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from carts.models import CartItem, Cart
from goods.serializers import GoodsSaleSerializers


class CartItemSerializer(ModelActionSerializer):
    sub_total = serializers.SerializerMethodField()
    discount_payment = serializers.SerializerMethodField()
    goods = GoodsSaleSerializers(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'goods', 'quantity', 'sub_total', 'discount_payment')
        examples = [{
            "id": 5,
            "cart": 1,
            "goods": {
                "id": 5,
                "title": "친환경 당근 500g",
                "short_desc": "껍질째 먹을 수 있는 친환경 흙당근 (500g 내외)",
                "packing_status": "냉장",
                "price": 2700,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EC%B9%9C%ED%99%98%EA%B2%BD%20%EB%8B%B9%EA%B7%BC%20500g/%EC%B9%9C%ED%99%98%EA%B2%BD_%EB%8B%B9%EA%B7%BC_500g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T183245Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=69a7d3efd0226123c485337c03cd4d60a99d8ef63e29e52cf63aeeb14867f406",
                "sales": {
                    "discount_rate": 35,
                    "contents": 'null'
                },
                "tagging": [],
                "discount_price": 1755
            },
            "quantity": 10,
            "sub_total": 27000,
            "discount_payment": 17550
        },
            {
                "id": 6,
                "cart": 1,
                "goods": {
                    "id": 6,
                    "title": "양배추 2종",
                    "short_desc": "달큰 아삭 하게 즐기는 양배추",
                    "packing_status": "냉장",
                    "price": 2600,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EC%96%91%EB%B0%B0%EC%B6%94%202%EC%A2%85/%EC%96%91%EB%B0%B0%EC%B6%94_2%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T183245Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4779d8a5f4061a05150fcd36641c191af6311374e60ed99cd6e1c17e2f835e46",
                    "sales": {
                        "discount_rate": 25,
                        "contents": 'null'
                    },
                    "tagging": [],
                    "discount_price": 1950
                },
                "quantity": 1,
                "sub_total": 2600,
                "discount_payment": 1950
            },
            {
                "id": 7,
                "cart": 1,
                "goods": {
                    "id": 7,
                    "title": "무 1통",
                    "short_desc": "시원한 무 한 통",
                    "packing_status": "냉장",
                    "price": 1980,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EB%AC%B4%201%ED%86%B5/%EB%AC%B4_1%ED%86%B5_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T183245Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=7e77fd8dca14650850e131c7849ea3db3d2db4be7acaea5225e75892b1b5df77",
                    "sales": {
                        "discount_rate": 'null',
                        "contents": "+gift"
                    },
                    "tagging": [],
                    "discount_price": 'null'
                },
                "quantity": 1,
                "sub_total": 1980,
                "discount_payment": 1980
            }, ]

    def get_sub_total(self, obj):
        return obj.sub_total

    def get_discount_payment(self, obj):
        return obj.discount_payment


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('goods', 'quantity', 'cart')
        examples = {
            "goods": 8,
            "quantity": 15,
            "cart": 1
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=CartItem.objects.all(),
                fields=('goods', 'cart'),
                message=("already exists instanace.")
            )
        ]

    def validate(self, attrs):
        return super().validate(attrs)


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True)
    total_pay = serializers.SerializerMethodField()
    discount_total_pay = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'quantity_of_goods', 'items', 'total_pay', 'discount_total_pay', 'discount_price')
        examples = {
            "id": 1,
            "quantity_of_goods": 4,
            "items": [
                {
                    "id": 5,
                    "cart": 1,
                    "goods": {
                        "id": 5,
                        "title": "친환경 당근 500g",
                        "short_desc": "껍질째 먹을 수 있는 친환경 흙당근 (500g 내외)",
                        "packing_status": "냉장",
                        "price": 2700,
                        "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EC%B9%9C%ED%99%98%EA%B2%BD%20%EB%8B%B9%EA%B7%BC%20500g/%EC%B9%9C%ED%99%98%EA%B2%BD_%EB%8B%B9%EA%B7%BC_500g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T180456Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=506418e858439659256a02ffa17a945d2ec899f2b393f3ba9c7293d941dac804",
                        "sales": {
                            "discount_rate": 35,
                            "contents": 'null'
                        },
                        "tagging": [],
                        "discount_price": 1755
                    },
                    "quantity": 10,
                    "sub_total": 27000,
                    "discount_payment": 17550
                },
                {
                    "id": 6,
                    "cart": 1,
                    "goods": {
                        "id": 6,
                        "title": "양배추 2종",
                        "short_desc": "달큰 아삭 하게 즐기는 양배추",
                        "packing_status": "냉장",
                        "price": 2600,
                        "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EC%96%91%EB%B0%B0%EC%B6%94%202%EC%A2%85/%EC%96%91%EB%B0%B0%EC%B6%94_2%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T180456Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=f02dd8eb21e3a217f2735e25d9e63365497a55ef6b56226d851588e29767379e",
                        "sales": {
                            "discount_rate": 25,
                            "contents": 'null'
                        },
                        "tagging": [],
                        "discount_price": 1950
                    },
                    "quantity": 1,
                    "sub_total": 2600,
                    "discount_payment": 1950
                },
                {
                    "id": 7,
                    "cart": 1,
                    "goods": {
                        "id": 7,
                        "title": "무 1통",
                        "short_desc": "시원한 무 한 통",
                        "packing_status": "냉장",
                        "price": 1980,
                        "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EB%AC%B4%201%ED%86%B5/%EB%AC%B4_1%ED%86%B5_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T180456Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=ebc5d2c26671ed1731cb63aa3b5ed0f1bab1b467dfc891f6380fb18af0bfed8d",
                        "sales": {
                            "discount_rate": 'null',
                            "contents": "+gift"
                        },
                        "tagging": [],
                        "discount_price": 'null'
                    },
                    "quantity": 1,
                    "sub_total": 1980,
                    "discount_payment": 1980
                }
            ],
            "total_pay": 31580,
            "discount_total_pay": 21480,
            "discount_price": 10100
        }

    def get_total_pay(self, obj):
        return obj.total_pay

    def get_discount_total_pay(self, obj):
        return obj.discount_total_pay

    def get_discount_price(self, obj):
        return int(obj.total_pay - obj.discount_total_pay)

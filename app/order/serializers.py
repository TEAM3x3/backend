from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from carts.models import CartItem
from carts.serializers import CartItemSerializer

from goods.serializers import GoodsSaleSerializers
from order.models import Order, OrderReview, OrderDetail

User = get_user_model()


class UserOrderSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class OrderDetailCreateSerializers(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = (
            'delivery_cost',
            'point',

            'consumer',
            'created_at',
            'receiver',
            'receiver_phone',
            'delivery_type',
            'zip_code',
            'address',
            'receiving_place',
            'entrance_password',
            'free_pass',
            'etc',

            'extra_message',
            'message',
            'payment_type',
        )

    def create(self, validated_data):
        ins = super().create(validated_data)
        ins.status = '결제완료'
        ins.title = f'{ins.order.items.first().goods.title} 외 {ins.order.items.count() - 1}건'
        items = ins.order.items.all()
        for item in items:
            cart = item.cart
            cart.quantity_of_goods = F('quantity_of_goods') - 1
            cart.save()
            item.cart = None
            item.save()
        ins.save()
        return ins


class OrderDetailSerializers(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = (
            'title',
            'delivery_cost',
            'point',

            'consumer',
            'created_at',
            'receiver',
            'receiver_phone',
            'delivery_type',
            'zip_code',
            'address',
            'receiving_place',
            'entrance_password',
            'free_pass',
            'etc',

            'extra_message',
            'message',
            'order',
            'payment_type'
        )


class OrderSerializers(ModelSerializer):
    total_payment = serializers.SerializerMethodField()
    discount_payment = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True)
    orderdetail = OrderDetailSerializers()
    user = UserOrderSerializers()

    class Meta:
        model = Order
        fields = (
            'id',
            'items',
            'total_payment',
            'discount_price',
            'discount_payment',
            'orderdetail',
            'user'
        )

    def get_total_payment(self, obj):
        return obj.total_payment

    def get_discount_payment(self, obj):
        return obj.discount_payment

    def get_discount_price(self, obj):
        return int(obj.total_payment - obj.discount_payment)


class OrderCreateSerializers(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'items',
        )

    def validate_items(self, value):
        for cart_item in value:
            if cart_item.goods.stock.count == 0:
                raise ValidationError('상품의 재고가 없습니다!')
        return value


class ReviewUpdateSerializers(ModelSerializer):
    class Meta:
        model = OrderReview
        fields = ('title', 'content', 'img',)
        examples = {
            "title": "update review title",
            "content": "update review content"
        }


class ReviewListSerializers(ModelSerializer):
    goods = GoodsSaleSerializers()
    user = UserOrderSerializers()

    class Meta:
        model = OrderReview
        fields = ('id', 'user', 'created_at', 'img', 'title', 'content', 'goods')
        examples = [
            {
                "id": 1,
                "title": "test create",
                "content": "contnet create",
                "goods": {
                    "id": 1,
                    "title": "[KF365] 햇 감자 1kg",
                    "short_desc": "믿고 먹을 수 있는 상품을 합리적인 가격에, KF365",
                    "packing_status": "상온",
                    "transfer": "샛별배송/택배배송",
                    "price": 2380,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKF365%5D%20%ED%96%87%20%EA%B0%90%EC%9E%90%201kg/KF365_%ED%96%87_%EA%B0%90%EC%9E%90_1kg_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T212332Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=d3539d90c6ef746312452ffb2dfc8d34af19b256bef3937204a66d4ff5e15664",
                    "sales": 'null',
                    "tagging": [],
                    "discount_price": 'null'
                }
            }
        ]


class ReviewCreateSerializers(ModelActionSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = OrderReview
        fields = ('id', 'title', 'content', 'goods', 'user')
        action_fields = {
            'create': {'fields': ('title', 'content', 'img', 'user', 'goods', 'cartItem')},
        }
        examples = {
            "title": "title exam",
            "content": "content exam",
            "goods": "2",
            "cartItem": "2"
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=OrderReview.objects.all(),
                # 유저는 특정 주문에 구매한 상품만 구매 가능
                fields=('user', 'goods', 'cartItem'),
                message="이미 작성한 리뷰 입니다."
            )
        ]

    def validate(self, attrs):
        goods_id = attrs['goods'].id
        user_id = attrs['user'].id
        cartItem_id = attrs['cartItem'].id
        try:
            cart_item_ins = CartItem.objects.get(pk=cartItem_id)
        except CartItem.DoesNotExist:
            raise serializers.ValidationError('존재하지 않은 cart item pk 입니다.')
        if cart_item_ins.status == 'w':
            raise serializers.ValidationError('상품 후기는 상품을 구매하시고, 배송이 완료된 회원 분만 한 달 내에 작성이 가능합니다.')
        qs = CartItem.objects.filter(status='c').filter(goods__id=goods_id).filter(order__user__id=user_id).filter(
            id=cartItem_id)
        if not qs.exists():
            raise serializers.ValidationError('리뷰 작성이 가능한 데이터가 존재하지 않습니다.')
        return super().validate(attrs)

    def validate_cartItem(self, value):
        return value

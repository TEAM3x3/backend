from action_serializer import ModelActionSerializer
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from carts.models import CartItem
from carts.serializers import CartItemSerializer
from goods.serializers import GoodsSaleSerializers
from members.serializers import UserOrderSerializers
from order.models import Order, OrderReview, OrderDetail


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
            'payment_type'
        )

    @transaction.atomic()
    def create(self, validated_data):
        ins = super().create(validated_data)
        ins.status = '결제완료'
        ins.save()
        return ins


class OrderDetailSerializers(ModelSerializer):
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
        fields = ('title', 'content')


class ReviewSerializers(ModelActionSerializer):
    goods_ins = GoodsSaleSerializers(source='goods')
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = OrderReview
        fields = ('id', 'title', 'content', 'goods', 'user')
        action_fields = {
            'list': {'fields': ('id', 'goods', 'title', 'content', 'goods_ins')},
            'create': {'fields': ('title', 'content', 'user', 'goods', 'cartItem')},
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
        qs = CartItem.objects.filter(status='c').filter(goods__id=goods_id).filter(order__user__id=user_id).filter(
            id=cartItem_id)
        if not qs.exists():
            raise serializers.ValidationError('리뷰 작성이 가능한 데이터가 존재하지 않습니다.')
        return super().validate(attrs)

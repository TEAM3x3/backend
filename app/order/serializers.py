from action_serializer import ModelActionSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carts.models import CartItem
from carts.serializers import CartItemSerializer
from goods.serializers import GoodsSaleSerializers
from members.serializers import UserSerializer, UserAddressSerializers
from order.models import Order, OrderReview


class OrderListSerializers(ModelSerializer):
    item = CartItemSerializer(many=True)
    user = UserSerializer()
    address = UserAddressSerializers()
    payment = serializers.SerializerMethodField()
    discount_payment = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  'status',
                  'payment',
                  'discount_payment',
                  'discount_price',
                  )

    def get_payment(self, obj):
        return obj.total_payment()

    def get_discount_payment(self, obj):
        return obj.discount_payment()

    def get_discount_price(self, obj):
        return int(obj.total_payment() - obj.discount_payment())


class OrderCreateSerializers(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'address',
                  'item',
                  )


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
        qs = CartItem.objects.filter(status='p').filter(order__user_id=user_id).filter(
            goods_id=goods_id)
        if not qs.exists():
            raise serializers.ValidationError('리뷰 작성이 가능한 데이터가 존재하지 않습니다.')
        return super().validate(attrs)

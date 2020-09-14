from action_serializer import ModelActionSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carts.models import CartItem
from carts.serializers import CartItemSerializer
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


class ReviewCreateSerializers(ModelActionSerializer):
    class Meta:
        model = OrderReview
        fields = ('id', 'title', 'content', 'goods', 'order', 'user')
        action_fields = {
            'list': {'fields': ('id', 'goods', 'title',)},
            'create': {'fields': ('title', 'content', 'goods', 'order', 'user')},
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=OrderReview.objects.all(),
                # 유저는 특정 주문에 구매한 상품만 구매 가능
                fields=('user', 'goods', 'order'),
                message="이미 작성한 리뷰 입니다."
            )
        ]

    def validate(self, attrs):
        goods = self.initial_data['goods']
        user = self.initial_data['user']
        order = self.initial_data['order']
        qs = CartItem.objects.filter(order__user__pk=user).filter(order__status='c') \
            .filter(goods__pk=goods).filter(order__pk=order)
        if qs.count() == 0:
            raise ValueError('리뷰 작성이 가능한 데이터가 존재하지 않습니다.')
        return super().validate(attrs)

    def validate_user(self, value):
        if self.context['request'].user != value:
            raise serializers.ValidationError('요청한 유저와 값을 받은 유저가 일치하지 않습니다.')
        return value

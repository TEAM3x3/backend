from django.contrib.auth import get_user_model
from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet
from carts.models import CartItem
from carts.serializers import CartItemListSerializer, CartItemCreateSerializer, \
    CartItemUpdateSerializer
from goods.models import Goods

User = get_user_model()


class CartViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer

    def get_queryset(self):
        if self.action == 'list':
            user = User.objects.first()
            return CartItem.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CartItemListSerializer
        elif self.action == 'create':
            return CartItemCreateSerializer
        elif self.action == 'patch':
            return CartItemUpdateSerializer

    # def add_cart(request, goods_pk):
    #     goods = Goods.objects.get(pk=goods_pk):




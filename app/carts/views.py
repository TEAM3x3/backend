from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from carts.models import CartItem, Cart
from carts.serializers import CartSerializer
from goods.models import Goods


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

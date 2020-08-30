from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from carts.models import CartItem, Cart
from carts.serializers import CartItemSerializer, CartSerializer

User = get_user_model()


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = User.objects.first()
        qs = self.queryset.filter(user=user)
        return qs
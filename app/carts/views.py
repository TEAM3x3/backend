from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from carts.models import CartItem
from carts.serializers import CartItemSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

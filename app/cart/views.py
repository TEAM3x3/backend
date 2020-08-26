from rest_framework.viewsets import ModelViewSet
from cart.models import Cart, CartItem
from cart.serializers import CartSerializers, CartItemSerializers


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers

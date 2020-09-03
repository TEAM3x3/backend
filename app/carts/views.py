from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from carts.models import CartItem, Cart
from carts.permissions import CartIsOwnerOrReadOnly, CartItemIsOwnerOrReadOnly
from carts.serializers import CartItemSerializer, CartSerializer, CartItemCreateSerializer

User = get_user_model()


class CartItemViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (CartItemIsOwnerOrReadOnly, )

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)


class CartViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (CartIsOwnerOrReadOnly, )

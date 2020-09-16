from django.contrib.auth import get_user_model
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=False, methods=['delete'])
    def goods_delete(self, request, *args, **kwargs):
        delete_items = request.data['goods']
        # user_all_items = CartItem.objects.all(user=request.user)
        items = CartItem.objects.filter(pk__in=delete_items)

        for i in items:
            items.delete()

        return Response("clear", status=status.HTTP_200_OK)


class CartViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (CartIsOwnerOrReadOnly, )


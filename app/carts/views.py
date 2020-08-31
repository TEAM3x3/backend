from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from carts.models import CartItem, Cart
from carts.serializers import CartItemSerializer, CartSerializer

User = get_user_model()


class CartItemViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = CartItem.objects.all()

    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        user = User.objects.first()
        qs = self.queryset.filter(user=user)
        return qs

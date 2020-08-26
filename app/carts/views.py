from django.contrib.auth import get_user_model
from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet
from carts.models import CartItem
from carts.serializers import CartItemSerializer

User = get_user_model()


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        if self.action == 'list':
            user = User.objects.first()
            return CartItem.objects.filter(user=user)

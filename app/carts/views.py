from django.contrib.auth import get_user_model
from requests import Response
from rest_framework import mixins, status

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from carts.models import CartItem
from carts.serializers import CartItemCreateSerializer, CartItemListSerializer, CartItemUpdateSerializer

User = get_user_model()


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer

    # def get_queryset(self):
    #     if self.action == 'list':
    #         user = User.objects.first()
    #         return CartItem.objects.filter(user=user)
    #     else:
    #         super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        elif self.action == 'patch':
            return CartItemUpdateSerializer
        else:
            return self.serializer_class

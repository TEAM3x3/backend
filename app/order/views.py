from rest_framework import mixins
<<<<<<< HEAD
from rest_framework.viewsets import ViewSet, GenericViewSet
=======
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from carts.models import CartItem
>>>>>>> aac0997f205ffeac4d97c8d453b3b32fde671294
from order.models import Order
from order.serializers import OrderCreateSerializers, OrderListSerializers


class OrderView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializers

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderListSerializers
        else:
            return self.serializer_class

<<<<<<< HEAD
=======
    def perform_create(self, serializer):
        items_pk = self.request.data['item']
        items_ins = CartItem.objects.filter(pk__in=items_pk)
        for item in items_ins:
            item.cart = None
            item.save()
        serializer.save()


class OrderAPIView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    1. order urls -> urls  /api/order
    2. view -> list, retrieve, create, destroy
    3. serialzier -> create // pk, list -> serializer

    """
>>>>>>> aac0997f205ffeac4d97c8d453b3b32fde671294

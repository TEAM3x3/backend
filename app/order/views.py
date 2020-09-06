from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderCreateSerializers, OrderListSerializers


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializers

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderListSerializers
        else:
            return self.serializer_class

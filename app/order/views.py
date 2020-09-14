from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from carts.models import CartItem
from order.models import Order, OrderReview
from order.serializers import OrderCreateSerializers, OrderListSerializers, ReviewCreateSerializers


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

    def get_queryset(self):
        try:
            if self.kwargs['user_pk']:
                return self.queryset.filter(user_id=self.kwargs['user_pk'])
        except KeyError:
            return super().get_queryset()

    # def perform_create(self, serializer):
    #     items_pk = self.request.data['item']
    #     items_ins = CartItem.objects.filter(pk__in=items_pk)
    #     for item in items_ins:
    #         item.cart = None
    #         item.save()
    #     serializer.save()


class ReviewAPI(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = OrderReview.objects.all()
    serializer_class = ReviewCreateSerializers

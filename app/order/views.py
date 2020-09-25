from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carts.models import CartItem
from carts.serializers import CartItemSerializer
from order.models import Order, OrderReview
from order.permissions import OrderReviewPermission
from order.serializers import OrderCreateSerializers, OrderListSerializers, ReviewSerializers, \
    ReviewUpdateSerializers


class OrderView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializers
    """
    결제가 완료 되면 order.status = 'd' 로 update
    결제 완료가 되고 하루 뒤 아침 7시에는 order.status='c' 로 update
    """

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
    serializer_class = ReviewSerializers
    """
    배송이 완료 되기 전 'r' ready
    배송 완료- 후기 작성 가능 상태 'p' possible
    후기 작성 완료 'd' done 
    """

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            goods_pk = self.kwargs['goods_pk']
            if goods_pk:
                return self.queryset.filter(goods_id=goods_pk)
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ['partial_update']:
            return ReviewUpdateSerializers
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [OrderReviewPermission(), ]
        # 참고 링크 :https://stackoverflow.com/questions/35970970/django-rest-framework-permission-classes-of-viewset-method
        return [permissions() for permissions in self.permission_classes]

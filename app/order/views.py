from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from order.models import Order, OrderReview, OrderDetail
from order.permissions import OrderReviewPermission, OrderPermission
from order.serializers import OrderCreateSerializers, ReviewSerializers, \
    ReviewUpdateSerializers, OrderSerializers, OrderDetailSerializers


class OrderView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializers
    permission_classes = (OrderPermission,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderSerializers
        else:
            return self.serializer_class

    def get_queryset(self):
        try:
            user_pk = self.kwargs['user_pk']
            if user_pk:
                return self.queryset.filter(user_id=self.kwargs['user_pk']).filter(orderdetail__status='배송완료')
        except KeyError:
            return super().get_queryset()


class OrderDetailView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializers


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

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from goods.models import Goods, Type, DeliveryInfo, Category
from goods.serializers import GoodsSerializers, DeliveryInfoSerializers, CategoriesSerializers


class GoodsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers

    def get_queryset(self):
        # 모든 상품에 대한 정보는 보여주지 않을 것 입니다.(의도치 않은 요청)
        qs = []
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            qs = self.queryset.filter(pk=pk)
        category = self.request.query_params.get('category', None)
        if category is not None:
            qs = self.queryset.filter(category__name=category)
        type_ins = self.request.query_params.get('type', None)
        if type_ins is not None:
            type_ins = Type.objects.filter(name=type_ins).first()
            qs = self.queryset.filter(types__type=type_ins)
        return qs

class DeliveryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = DeliveryInfo.objects.all()
    serializer_class = DeliveryInfoSerializers


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers

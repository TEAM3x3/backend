from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from goods.models import Goods
from goods.serializers import GoodsSerializers


class GoodsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers

import random
from django.db.models import Max
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from goods.filters import GoodsFilter
from goods.models import Goods, Type, Category, DeliveryInfoImageFile
from goods.serializers import GoodsSerializers, DeliveryInfoSerializers, CategoriesSerializers, GoodsSaleSerializers
from django_filters.rest_framework import DjangoFilterBackend


class GoodsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers
    # filter는 각 viewset별 다를 수 있어서
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = GoodsFilter
    ordering_fields = ['price', ]

    def get_serializer_class(self):
        if self.action == 'sale':
            return GoodsSaleSerializers
        else:
            return super().serializer_class

    def filter_queryset(self, queryset):
        # 모든 상품에 대한 정보는 보여주지 않을 것 입니다.(의도치 않은 요청)
        qs = None
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

    @action(detail=False)
    def main_page_md(self, request, *args, **kwargs):
        main_md = Goods.objects.filter(id=1)
        serializer = GoodsSerializers(main_md, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def main_page_health(self, request, *args, **kwargs):
        main_health = Goods.objects.filter(category__name='건강식품')
        serializer = GoodsSerializers(main_health, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def main_page_recommend(self, request, *args, **kwargs):
        max_id = Goods.objects.all().count()
        recommend_items = []

        while True:
            # 1 , 1256
            random_pk = random.randint(1, max_id)
            if random_pk in recommend_items:
                continue
            else:
                recommend_items.append(random_pk)
            if len(recommend_items) == 6:
                break

        qs = Goods.objects.filter(pk__in=recommend_items)
        serializer = GoodsSerializers(qs, many=True)

    @action(detail=False, url_path='sale', )
    def sale(self, request):
        qs = self.queryset.filter(sales__discount_rate__isnull=False)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class DeliveryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = DeliveryInfoImageFile.objects.all()
    serializer_class = DeliveryInfoSerializers


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers

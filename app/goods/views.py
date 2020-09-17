import secrets
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from goods.models import Goods, Type, Category, DeliveryInfoImageFile
from goods.serializers import GoodsSerializers, DeliveryInfoSerializers, CategoriesSerializers, GoodsSaleSerializers
from rest_framework.filters import OrderingFilter


class GoodsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSaleSerializers
    # filter는 각 viewset별 다를 수 있어서
    filter_backends = (OrderingFilter,)
    ordering_fields = ['price', ]
    filterset_fields = ['goods', ]

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return GoodsSerializers
        else:
            return self.serializer_class

    def get_queryset(self):
        qs = None
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            qs = self.queryset.filter(pk=pk)
        category = self.request.query_params.get('category', None)
        if category is not None:
            qs = self.queryset.filter(types__type__category__name=category)
        type_ins = self.request.query_params.get('type', None)
        if type_ins is not None:
            type_ins = Type.objects.filter(name=type_ins).first()
            qs = self.queryset.filter(types__type=type_ins)
        sale = self.request.query_params.get('sale', None)
        if sale is not None:
            qs = self.queryset.filter(sales__discount_rate__isnull=False)
        return qs

    @action(detail=False)
    def main_page_md(self, request, *args, **kwargs):
        main_md = Goods.objects.filter(id=1)
        serializer = GoodsSaleSerializers(main_md, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def main_page_health(self, request, *args, **kwargs):
        main_health = Goods.objects.filter(category__name='건강식품')
        serializer = GoodsSaleSerializers(main_health, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def main_page_recommend(self, request, *args, **kwargs):
        max_id = Goods.objects.all().count()
        recommend_items = []

        while True:
            # 1 , 1256
            random_pk = secrets.randbelow(max_id)
            if random_pk in recommend_items:
                continue
            elif max_id == 0:
                continue
            else:
                recommend_items.append(random_pk)
            if len(recommend_items) == 8:
                break

        qs = Goods.objects.filter(pk__in=recommend_items)
        serializer = GoodsSerializers(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='sale', )
    def sale(self, request):
        # issue
        # viewset에 설정한 filter_backends = (OrderingFilter,)가 get_queryset에선 동작하나 여기서는 동작 하지 않음.
        # order_by를 통하여 해결을 하였으나 성능에 대한 이슈 제기.
        # get_queryset에서 params에 sale을 받는 형식으로 하면 동작 가능하지만 올바르지 않은 접근 같다고 판단 하였습니다.
        qs = self.queryset.filter(sales__discount_rate__isnull=False)
        params = self.request.query_params.get('ordering', None)
        if params is not None:
            qs = qs.order_by(params)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def goods_search(self, request, *args, **kwargs):
        word = self.request.GET.get('word', '')
        if word:
            qs = self.queryset.filter(title__icontains=word)
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeliveryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = DeliveryInfoImageFile.objects.all()
    serializer_class = DeliveryInfoSerializers


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers

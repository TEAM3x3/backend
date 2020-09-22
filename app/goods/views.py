import random
import secrets
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from goods.models import Goods, Type, Category, DeliveryInfoImageFile
from goods.serializers import GoodsSerializers, DeliveryInfoSerializers, CategoriesSerializers, GoodsSaleSerializers
from rest_framework.filters import OrderingFilter
from members.models import UserSearch, KeyWord
from order.models import OrderReview
from order.serializers import ReviewSerializers


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
        id = self.kwargs.get('pk', None)
        if id:
            qs = self.queryset.filter(id=id)
        category = self.request.query_params.get('category', None)
        if category:
            qs = self.queryset.filter(types__type__category__name=category)
        type_ins = self.request.query_params.get('type', None)
        if type_ins:
            type_ins = Type.objects.filter(name=type_ins).first()
            qs = self.queryset.filter(types__type=type_ins)
        sale = self.request.query_params.get('sale', None)
        if sale:
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
            elif random_pk == 0:
                continue
            else:
                recommend_items.append(random_pk)
            if len(recommend_items) == 8:
                break

        qs = Goods.objects.filter(id__in=recommend_items)
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
        if params:
            qs = qs.order_by(params)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def goods_search(self, request, *args, **kwargs):
        search_word = self.request.GET.get('word', '')
        if search_word:
            # 유저는 '가지'라는 키워드를 검색
            # 유저는 최근 검색어 '가지'
            # '가지'라는 키워드는 1번 검색이 됨
            # word_ins, __Keyword.objects.get_or_create(
            # UserSearch.objects.create(user=requset.user, keyword=word_ins)
            key_word, __ = KeyWord.objects.get_or_create(name=search_word)
            word = UserSearch.objects.create(user=request.user, keyword=key_word)
            qs = self.queryset.filter(title__icontains=key_word)
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def sales_goods(self, request, *args, **kwargs):
        count_all = self.queryset.filter(sales__discount_rate__isnull=False).count()
        sales_items = []

        while True:
            # 1 , 716
            random_save = random.randint(count_all)
            if random_save in sales_items:
                continue
            elif random_save == 0:
                continue
            else:
                sales_items.append(random_save)
            if len(sales_items) == 8:
                break
        save_ins = self.queryset.filter(pk__in=sales_items)
        serializer = GoodsSaleSerializers(save_ins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def reviews(self, request, *args, **kwargs):
        goods_pk = kwargs['pk']
        qs = OrderReview.objects.filter(goods__pk=goods_pk)
        serializers = ReviewSerializers(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers


class DeliveryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = DeliveryInfoImageFile.objects.all()
    serializer_class = DeliveryInfoSerializers

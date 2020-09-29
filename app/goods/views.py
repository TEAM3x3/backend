import random
import secrets

import django_filters
from rest_framework import mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from goods.filters import GoodsFilter
from goods.models import Goods, Category
from goods.serializers import GoodsSerializers, CategoriesSerializers, GoodsSaleSerializers
from members.models import UserSearch, KeyWord
from members.serializers import UserSearchSerializer
from order.models import OrderReview
from order.serializers import ReviewSerializers


class GoodsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSaleSerializers
    # filter는 각 viewset별 다를 수 있어서
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ['price', 'sales__discount_rate']
    filter_class = GoodsFilter

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return GoodsSerializers
        else:
            return self.serializer_class

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
        qs = self.queryset.filter(sales__discount_rate__isnull=False)
        qs = self.filter_queryset(qs)
        serializers = self.get_serializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def goods_search(self, request, *args, **kwargs):
        search_word = self.request.GET.get('word', None)
        if search_word:
            key_word, __ = KeyWord.objects.get_or_create(name=search_word)
            user_search_data = {
                "keyword": key_word.id,
                "user": request.user.id
            }

            try:
                search_ins = UserSearch.objects.get(user=request.user, keyword=key_word)
                serializers = UserSearchSerializer(search_ins, data=user_search_data, partial=True)
            except UserSearch.DoesNotExist:
                serializers = UserSearchSerializer(data=user_search_data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            # word = UserSearch.objects.create(user=request.user, keyword=key_word)

            qs = self.queryset.filter(title__icontains=key_word)
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def sales_goods(self, request, *args, **kwargs):
        count_all = self.queryset.filter(sales__discount_rate__isnull=False).count()
        max_random_item_count = 8
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
            if len(sales_items) == max_random_item_count:
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

    @action(detail=False)
    def best(self, request):
        """
        - ordering //
            # 신상품 순 qs = sorted(qs, key=lambda value: value.stock.updated_at),
            # 판매 순, 내림차순 qs = sorted(qs, key=lambda value: value.sales_count, reverse = True),
            # 가격 내림차순 qs = sorted(qs, key=lambda value: value.price, reverse=True),
            # 가격 오름차순 qs = sorted(qs, key=lambda value: value.price)
        """
        transfer = request.query_params.get('transfer', None)
        ordering = request.query_params.get('ordering', None)
        qs = self.queryset.order_by('-sales_count')[:30]
        transfer_qs = []
        for obj in qs:
            if obj.transfer == transfer:
                transfer_qs.append(obj)
        transfer_qs = sorted(transfer_qs, key=lambda value: f'value.{ordering}')
        serializers = self.serializer_class(transfer_qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers

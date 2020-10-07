import random
import secrets

import django_filters
from rest_framework import mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.instructors import MyAutoSchema
from goods.filters import GoodsFilter
from goods.models import Goods, Category
from goods.serializers import GoodsSerializers, GoodsSaleSerializers, CategoryGoodsSerializers, CategorySerializers, \
    GoodsReviewSerializers, CategoriesSerializers
from members.models import UserSearch, KeyWord
from members.serializers import UserSearchSerializer
from collections import defaultdict


class GoodsViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSaleSerializers
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ['price', 'sales__discount_rate']
    filter_class = GoodsFilter
    swagger_schema = MyAutoSchema

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return GoodsSerializers
        else:
            return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        상품 리스트

        -----
        데이터 정렬 순서

        배송 정보 > transfer # '샛별배송 ONLY', '샛별배송/택배배송', null 중 1

        할인이 적용된 가격 > discount_price # 할인률이 없으면 None

        원가 > price

        할인률 sales > discount_rate

        상품 판매율 > sales_count

        신상품 순 > stock > updated_at

        # 카테고리별 상품 분류

        - http://13.209.33.72/api/goods?category=<category_name>

        # 타입별 상품 분류

        - http://13.209.33.72/api/goods?type=<type_name>



        ```
        [
            {
                "id": 105,
                "title": "유기농 무화과 600g",
                "short_desc": "인류가 재배한 최초의 과일(600g/1팩)",
                "packing_status": "냉장",
                "transfer": "샛별배송/택배배송",
                "price": 10500,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EC%9C%A0%EA%B8%B0%EB%86%8D%20%EB%AC%B4%ED%99%94%EA%B3%BC%20600g/%EC%9C%A0%EA%B8%B0%EB%86%8D_%EB%AC%B4%ED%99%94%EA%B3%BC_600g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T160935Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=6ffb03aefb8669172cc67e57bf66cd2d96f531d53594bbac293e9893eff95add",
                "sales": {
                    "discount_rate": 10,
                    "contents": null
                },
                "tagging": [],
                "discount_price": 9450,
                "sales_count": 6,
                "stock": {
                    "id": 105,
                    "count": 39,
                    "updated_at": "2020-08-03T18:04:20.951000Z"
                }
            },
            {
                "id": 106,
                "title": "허니듀 멜론 1.8kg 이상",
                "short_desc": "하니원 멜론에 이어 이름 처럼 달콤한",
                "packing_status": "냉장",
                "transfer": "샛별배송 ONLY",
                "price": 8400,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%ED%97%88%EB%8B%88%EB%93%80%20%EB%A9%9C%EB%A1%A0%201.8kg%20%EC%9D%B4%EC%83%81/%ED%97%88%EB%8B%88%EB%93%80_%EB%A9%9C%EB%A1%A0_1.8kg_%EC%9D%B4%EC%83%81_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T160935Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=d40dfbf65d891f2fea37f51be04c6af4a31029972c706f59583001b852c766e1",
                "sales": null,
                "tagging": [],
                "discount_price": null,
                "sales_count": 82,
                "stock": {
                    "id": 106,
                    "count": 9,
                    "updated_at": "2020-09-14T18:04:20.956000Z"
                }
            },
            {
                "id": 107,
                "title": "GAP 거봉포도 1팩",
                "short_desc": "여름을 알리는 달콤한 과즙(1팩/600g내외)",
                "packing_status": "냉장",
                "transfer": null,
                "price": 12900,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/GAP%20%EA%B1%B0%EB%B4%89%ED%8F%AC%EB%8F%84%201%ED%8C%A9/GAP_%EA%B1%B0%EB%B4%89%ED%8F%AC%EB%8F%84_1%ED%8C%A9_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T160935Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=29d7191b79a02548e26f3a8eb1187f29dc08010d7b7e6461d89c17c19564077f",
                "sales": {
                    "discount_rate": null,
                    "contents": "1+1"
                },
                "tagging": [],
                "discount_price": 7740,
                "sales_count": 64,
                "stock": {
                    "id": 107,
                    "count": 90,
                    "updated_at": "2020-08-27T18:04:39.654000Z"
                }
            }
            ...
        ]
        ```
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        상품 디테일 페이지

        ----
        상품 디테일 api 입니다.
        """
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False)
    def main_page_health(self, request, *args, **kwargs):
        """
        홈 - 컬리추천 건강식품[면역력 증진] API

        ---
        정렬 데이터 api/goods/best 참고
        ```
        [
            {
                "id": 611,
                "title": "[바로이즙] ABC 착즙주스 2종",
                "short_desc": "세 가지 과채의 영양이 그대로!",
                "packing_status": "상온",
                "transfer": "샛별배송/택배배송",
                "price": 9900,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%A1%9C%EC%9D%B4%EC%A6%99%5D%20ABC%20%EC%B0%A9%EC%A6%99%EC%A3%BC%EC%8A%A4%202%EC%A2%85/%EB%B0%94%EB%A1%9C%EC%9D%B4%EC%A6%99_ABC_%EC%B0%A9%EC%A6%99%EC%A3%BC%EC%8A%A4_2%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T171717Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=a75825426c04179910b7872a9d20ae0b90287b59e87a7f83f98603eb2c52451d",
                "sales": null,
                "tagging": [
                    {
                        "tag": {
                            "name": "한정수량"
                        }
                    }
                ],
                "discount_price": null,
                "sales_count": 94,
                "stock": {
                    "id": 611,
                    "count": 77,
                    "updated_at": "2020-08-15T18:04:28.297000Z"
                }
            },
            {
                "id": 797,
                "title": "[채움] 국내산 과일채소로 만든 주스 4종 (10개입)",
                "short_desc": "[박스판매] 100% 국내산 재료로 채운 주스 한 잔",
                "packing_status": null,
                "transfer": "샛별배송/택배배송",
                "price": 10800,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EC%B1%84%EC%9B%80%5D%20%EA%B5%AD%EB%82%B4%EC%82%B0%20%EA%B3%BC%EC%9D%BC%EC%B1%84%EC%86%8C%EB%A1%9C%20%EB%A7%8C%EB%93%A0%20%EC%A3%BC%EC%8A%A4%204%EC%A2%85%20%2810%EA%B0%9C%EC%9E%85%29/%EC%B1%84%EC%9B%80_%EA%B5%AD%EB%82%B4%EC%82%B0_%EA%B3%BC%EC%9D%BC%EC%B1%84%EC%86%8C%EB%A1%9C_%EB%A7%8C%EB%93%A0_%EC%A3%BC%EC%8A%A4_4%EC%A2%85_10%EA%B0%9C%EC%9E%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T171717Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b9a57561dc4082ad01fa716da45c02c5a051698f5e7838e6e16368b17e72d94a",
                "sales": null,
                "tagging": [],
                "discount_price": null,
                "sales_count": 68,
                "stock": {
                    "id": 797,
                    "count": 38,
                    "updated_at": "2020-07-26T18:04:30.799000Z"
                }
            },
            ...
        ]
        ```
        """
        main_health = Goods.objects.filter(types__type__category__name='건강식품').prefetch_related('event', 'tagging',
                                                                                                'stock', 'sales',
                                                                                                'tagging__tag',)
        serializer = GoodsSaleSerializers(main_health, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def main_page_recommend(self, request, *args, **kwargs):
        """
        홈 - 컬리추천 - 이 상품 어때요 API

        ---
        매 요청 마다 전체 상품에서 랜덤으로 8개의 상품 리턴합니다.

        예시는 다른 상품 api들과 형식이 동일합니다.
        """
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

        qs = Goods.objects.filter(id__in=recommend_items).prefetch_related('tagging__tag', 'stock', 'sales')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='sale', )
    def sale(self, request):
        """
        홈 - 알뜰 쇼핑

        -----
        best endpoint를 제외한, 양식 및 요청 동일
        """
        qs = self.queryset.filter(sales__discount_rate__isnull=False).prefetch_related('tagging__tag', 'stock', 'sales')
        qs = self.filter_queryset(qs)
        serializers = self.get_serializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def word_search(self, request):
        """
        검색 - 타이핑 단어에 포함된 상품 리턴 api

        ---
        request 에제 > /api/goods/word_search?word=간식

        params로 전송 바랍니다. key 값은 word 입니다.

        ```
        [
            {
                "id": 1142,
                "title": "[프로젝트21] 짜먹는 간식 리얼스틱 7종",
                "short_desc": "신선한 주재료를 가득히 담아낸 (생후 3개월 이상)",
                "packing_status": "상온",
                "transfer": "샛별배송/택배배송",
                "price": 5000,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B821%5D%20%EC%A7%9C%EB%A8%B9%EB%8A%94%20%EA%B0%84%EC%8B%9D%20%EB%A6%AC%EC%96%BC%EC%8A%A4%ED%8B%B1%207%EC%A2%85/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B821_%EC%A7%9C%EB%A8%B9%EB%8A%94_%EA%B0%84%EC%8B%9D_%EB%A6%AC%EC%96%BC%EC%8A%A4%ED%8B%B1_7%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T180327Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e0ee7508784a8c858d0dd657a00968458595e693270b5a1074d71ea03b8278a3",
                "sales": {
                    "discount_rate": 10,
                    "contents": null
                },
                "tagging": [
                    {
                        "tag": {
                            "name": "kurly's only"
                        }
                    }
                ],
                "discount_price": 4500,
                "sales_count": 76,
                "stock": {
                    "id": 1142,
                    "count": 76,
                    "updated_at": "2020-09-16T18:04:35.439000Z"
                }
            },
            {
                "id": 1147,
                "title": "[복슬강아지] 수제 냉동 간식 6종",
                "short_desc": "수분을 머금은 원물 간식 (생후 3개월 이상)",
                "packing_status": "냉동",
                "transfer": "샛별배송/택배배송",
                "price": 5000,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B3%B5%EC%8A%AC%EA%B0%95%EC%95%84%EC%A7%80%5D%20%EC%88%98%EC%A0%9C%20%EB%83%89%EB%8F%99%20%EA%B0%84%EC%8B%9D%206%EC%A2%85/%EB%B3%B5%EC%8A%AC%EA%B0%95%EC%95%84%EC%A7%80_%EC%88%98%EC%A0%9C_%EB%83%89%EB%8F%99_%EA%B0%84%EC%8B%9D_6%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T180327Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b9c13954863041149bf265da88b9aedd195eb1fb05eed35ab58e031719fae9d8",
                "sales": {
                    "discount_rate": 30,
                    "contents": null
                },
                "tagging": [],
                "discount_price": 3500,
                "sales_count": 8,
                "stock": {
                    "id": 1147,
                    "count": 85,
                    "updated_at": "2020-07-12T18:04:35.511000Z"
                }
            },
            ...
        ]
        ```
        """
        word = request.query_params.get('word', None)
        if not word:
            return Response({"message": "word가 전송되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        qs = Goods.objects.filter(title__icontains=word)
        serializers = self.get_serializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def goods_search(self, request, *args, **kwargs):
        """
        검색 - 검색어 입력 시 , 최근 검색어에 포함되는 API

        ---
        - 예시 ```/api/goods/goods_search?word=간식```

        - 토큰이 필요한 요청입니다.

        response examples는 검색 - 단어 검색 ```goods/word_search``` 와 일치합니다.

        """
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

            qs = self.queryset.filter(title__icontains=key_word).select_related('sales').prefetch_related('tagging',
                                                                                                          'stock',
                                                                                                          'tagging__tag')
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "word에 대한 데이터가 들어오지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def sales_goods(self, request, *args, **kwargs):
        """
        홈 - 컬리 추천에 위치한 알뜰 상품에 대한 상품 리스트

        ---
        - 할인률을 가진 8개의 상품이 매 요청마다 다르게 출력됩니다.
        - 필터링에 필요한 요청은 /goods/best에 작성한 글을 참고 바랍니다.

        ```
        [
            {
                "id": 231,
                "title": "[마켓베라즈] 생새우 2종(냉동)",
                "short_desc": "깔끔한 손질, 다양한 쓰임새",
                "packing_status": null,
                "transfer": "샛별배송/택배배송",
                "price": 10000,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%A7%88%EC%BC%93%EB%B2%A0%EB%9D%BC%EC%A6%88%5D%20%EC%83%9D%EC%83%88%EC%9A%B0%202%EC%A2%85%28%EB%83%89%EB%8F%99%29/%EB%A7%88%EC%BC%93%EB%B2%A0%EB%9D%BC%EC%A6%88_%EC%83%9D%EC%83%88%EC%9A%B0_2%EC%A2%85%EB%83%89%EB%8F%99_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T165731Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=1fcad4fd18e17493689ff03e59ab019ad766e4ea6b168f61777b9fc44ed5d13a",
                "sales": {
                    "discount_rate": 5,
                    "contents": null
                },
                "tagging": [],
                "discount_price": 9500,
                "sales_count": 76,
                "stock": {
                    "id": 231,
                    "count": 63,
                    "updated_at": "2020-06-30T18:04:22.696000Z"
                }
            },
            ...
        ]
        ```
        """
        count_all = self.queryset.filter(sales__discount_rate__isnull=False).count()
        max_random_item_count = 8
        sales_items = []

        while True:
            # 1 , 716
            random_save = random.randint(1, count_all)
            if random_save in sales_items:
                continue
            elif random_save == 0:
                continue
            else:
                sales_items.append(random_save)
            if len(sales_items) == max_random_item_count:
                break
        save_ins = self.queryset.filter(pk__in=sales_items).prefetch_related('tagging', 'sales', 'stock',
                                                                             'tagging__tag')
        serializer = GoodsSaleSerializers(save_ins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def best(self, request):
        """
        홈 - 베스트 상품

        ---

        배송 정보 : transfer # '샛별배송 ONLY', '샛별배송/택배배송', null 중 1

        할인이 있는 상품 : discount_price

        할인이 없는 상품 : price

        신상품 stock > updated_at

        판매량 : sales_count

        할인률 : sales > discount_rate

        ```
        [
            {
                "id": 300,
                "title": "[경주축협] 경주천년한우 1++등급 치마살 200g",
                "short_desc": "100g 당 판매가: 22,800원",
                "packing_status": "냉장",
                "transfer": "샛별배송/택배배송",
                "price": 45600,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EA%B2%BD%EC%A3%BC%EC%B6%95%ED%98%91%5D%20%EA%B2%BD%EC%A3%BC%EC%B2%9C%EB%85%84%ED%95%9C%EC%9A%B0%201%2B%2B%EB%93%B1%EA%B8%89%20%EC%B9%98%EB%A7%88%EC%82%B4%20200g/%EA%B2%BD%EC%A3%BC%EC%B6%95%ED%98%91_%EA%B2%BD%EC%A3%BC%EC%B2%9C%EB%85%84%ED%95%9C%EC%9A%B0_1%EB%93%B1%EA%B8%89_%EC%B9%98%EB%A7%88%EC%82%B4_200g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T163750Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=15a4f42c677ce9dd9c6e5b3eb2852a9e5d74074735006df880962112d7074664",
                "sales": {
                    "discount_rate": null,
                    "contents": "+gift"
                },
                "tagging": [],
                "discount_price": null,
                "sales_count": 99,
                "stock": {
                    "id": 300,
                    "count": 98,
                    "updated_at": "2020-07-14T18:04:23.870000Z"
                }
            },
            {
                "id": 444,
                "title": "[푸드렐라] 석쇠닭갈비",
                "short_desc": "쫄깃한 닭다리살에 불맛을 입힌 직화 닭갈비",
                "packing_status": "냉동",
                "transfer": "샛별배송/택배배송",
                "price": 7120,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%ED%91%B8%EB%93%9C%EB%A0%90%EB%9D%BC%5D%20%EC%84%9D%EC%87%A0%EB%8B%AD%EA%B0%88%EB%B9%84/%ED%91%B8%EB%93%9C%EB%A0%90%EB%9D%BC_%EC%84%9D%EC%87%A0%EB%8B%AD%EA%B0%88%EB%B9%84_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T163750Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=65fcf601f8705c370977ab4d44d98bc9385b4de09a427599e99648cc951cb293",
                "sales": {
                    "discount_rate": 40,
                    "contents": null
                },
                "tagging": [],
                "discount_price": 4272,
                "sales_count": 99,
                "stock": {
                    "id": 444,
                    "count": 40,
                    "updated_at": "2020-07-11T18:04:25.950000Z"
                }
            },
            {
                "id": 111,
                "title": "GAP 햇사과 한봉지 (자홍) 5~6입",
                "short_desc": "달콤 상콤한 제철사과 자홍! 5~6입 봉",
                "packing_status": "냉장",
                "transfer": "샛별배송/택배배송",
                "price": 8184,
                "img": "https://pbs-13-s3.s3.amazonaws.com/goods/GAP%20%ED%96%87%EC%82%AC%EA%B3%BC%20%ED%95%9C%EB%B4%89%EC%A7%80%20%28%EC%9E%90%ED%99%8D%29%205~6%EC%9E%85/GAP_%ED%96%87%EC%82%AC%EA%B3%BC_%ED%95%9C%EB%B4%89%EC%A7%80_%EC%9E%90%ED%99%8D_56%EC%9E%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T163750Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=aaed0ec6587ed09f0704378bec65cb4c7da1e5838be9d4e300ea91a816c05422",
                "sales": {
                    "discount_rate": 45,
                    "contents": null
                },
                "tagging": [],
                "discount_price": 4501,
                "sales_count": 99,
                "stock": {
                    "id": 111,
                    "count": 9,
                    "updated_at": "2020-08-12T18:04:20.997000Z"
                }
            },
            ...
        ]
        ```
        """
        # transfer = request.query_params.get('transfer', None)
        # ordering = request.query_params.get('ordering', None)
        qs = self.queryset.order_by('-sales_count')[:30].prefetch_related('tagging', 'sales', 'stock', 'tagging__tag')
        # transfer_qs = []
        # for obj in qs:
        #     if obj.transfer == transfer:
        #         transfer_qs.append(obj)
        # transfer_qs = sorted(transfer_qs, key=lambda value: f'value.{ordering}')
        serializers = self.serializer_class(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def recommend_review(self, request):
        """
        추천- 후기가 좋은 상품 API

        ----
        ```
        [
            {
                "id": 1,
                "title": "친환경 당근 500g",
                "price": 2700,
                "info_img": "https://pbs-13-s3.s3.amazonaws.com/goods/%EC%B9%9C%ED%99%98%EA%B2%BD%20%EB%8B%B9%EA%B7%BC%20500g/%EC%B9%9C%ED%99%98%EA%B2%BD_%EB%8B%B9%EA%B7%BC_500g_info_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201005%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201005T143448Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=88c8b1f9860369545e8aa4ceedd21eefed56f5a9c3339a21403190174920ad6e",
                "reviews": [
                    {
                        "id": 16,
                        "title": "추천합니다!!!!!!!",
                        "content": "추천합니다!!!!!!! 에 대한 내용입니다.",
                        "user": {
                            "username": "admin"
                        }
                    },
                    ...(다른 리뷰들)
                ]
            }
            ...(다른 상품들 - 상품에 해당하는 리뷰들)
        ]
        ```
        """
        qs = self.queryset[:5].prefetch_related('reviews__user__order_set')
        serializers = GoodsReviewSerializers(qs, many=True)
        data = {
            "title": "후기가 좋은 상품",
            "serializers": serializers.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, )
    def cleaning(self, request):
        """
        추천 - 집안 구석구석 쾌적하게 API

        ---
        추천에 해당하는 이름은 # 집안 구석구석 쾌적하게 입니다. 매 요청마다 다른 청소 용품들을 돌려줍니다.
        ```
        {
            "bool": "false",
            "serializers": [
                {
                    "id": 895,
                    "title": "[레인보우샵] 과탄산소다 4종",
                    "short_desc": "순하지만 강한 친환경 표백제",
                    "packing_status": "상온",
                    "transfer": "샛별배송/택배배송",
                    "price": 2400,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%A0%88%EC%9D%B8%EB%B3%B4%EC%9A%B0%EC%83%B5%5D%20%EA%B3%BC%ED%83%84%EC%82%B0%EC%86%8C%EB%8B%A4%204%EC%A2%85/%EB%A0%88%EC%9D%B8%EB%B3%B4%EC%9A%B0%EC%83%B5_%EA%B3%BC%ED%83%84%EC%82%B0%EC%86%8C%EB%8B%A4_4%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201005%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201005T154555Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=fbfaf351c05d97554139846af305d0126cb2bdcedf54608daa5012e199599b4b",
                    "sales": {
                        "discount_rate": 45,
                        "contents": null
                    },
                    "tagging": [],
                    "discount_price": 1320,
                    "sales_count": 11,
                    "stock": {
                        "id": 895,
                        "count": 29,
                        "updated_at": "2020-09-24T18:04:32.521000Z"
                    }
                },
                ...(추가 상품 데이터)
            ]
        }
        ```
        """
        lst = []
        list_length_limit = 5
        while True:
            random_pk = random.randint(894, 909)
            if random_pk in lst:
                continue
            elif random_pk == 0:
                continue
            else:
                lst.append(random_pk)
            if len(lst) == list_length_limit:
                break

        qs = Goods.objects.filter(id__in=lst)
        serializer = self.get_serializer(qs, many=True)
        data = {
            "bool": False,
            "title": "집안 구석구석 쾌적하게",
            "serializers": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, )
    def rice_cake(self, request):
        """
        추천 - 맛있는 떡 드셔보세요 API

        ---
        추천에 해당하는 이름은 # 맛있는 떡 드셔보세요 입니다. 매 요청마다 다른 상품들을 돌려줍니다.
        ```
        {
            "bool": "false",
            "serializers": [
                {
                    "id": 679,
                    "title": "[착한떡] 아기 찰떡바게트 3종",
                    "short_desc": "속이 쫀득한 오븐 베이킹 바게트",
                    "packing_status": "냉동",
                    "transfer": "샛별배송/택배배송",
                    "price": 1000,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EC%B0%A9%ED%95%9C%EB%96%A1%5D%20%EC%95%84%EA%B8%B0%20%EC%B0%B0%EB%96%A1%EB%B0%94%EA%B2%8C%ED%8A%B8%203%EC%A2%85/%EC%B0%A9%ED%95%9C%EB%96%A1_%EC%95%84%EA%B8%B0_%EC%B0%B0%EB%96%A1%EB%B0%94%EA%B2%8C%ED%8A%B8_3%EC%A2%85_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201005%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201005T154440Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=d98acc10fc647a95a8055d10475dac663cdf9a35d7d8a242372415f0d0d13e66",
                    "sales": {
                        "discount_rate": null,
                        "contents": "1+1"
                    },
                    "tagging": [
                        {
                            "tag": {
                                "name": "kurly's only"
                            }
                        }
                    ],
                    "discount_price": null,
                    "sales_count": 17,
                    "stock": {
                        "id": 679,
                        "count": 63,
                        "updated_at": "2020-07-17T18:04:29.358000Z"
                    }
                },
                ...(추가 상품 데이터)
            ]
        }
        ```
        """
        lst = []
        qs_list = []
        list_length_limit = 5
        qs = Goods.objects.filter(title__icontains='떡')
        while True:
            random_pk = random.randint(0, 20)
            if random_pk in lst:
                continue
            elif random_pk == 0:
                continue
            else:
                lst.append(random_pk)
                qs_list.append(qs[random_pk])
            if len(lst) == list_length_limit:
                break
        serializer = self.get_serializer(qs_list, many=True)
        data = {
            "bool": False,
            "title": "맛있는 떡 드셔보세요",
            "serializers": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False)
    def pet_goods_best(self, request):
        """
        추천 - 반려동물 판매 랭킹

        ----
        ```
            "bool": "false",
            "serializers": [
                {
                    "id": 1178,
                    "title": "[어플라우즈] 통살 참치",
                    "short_desc": "도톰 촉촉한 고양이 간식",
                    "packing_status": "상온",
                    "transfer": "샛별배송/택배배송",
                    "price": 3200,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EC%96%B4%ED%94%8C%EB%9D%BC%EC%9A%B0%EC%A6%88%5D%20%ED%86%B5%EC%82%B4%20%EC%B0%B8%EC%B9%98/%EC%96%B4%ED%94%8C%EB%9D%BC%EC%9A%B0%EC%A6%88_%ED%86%B5%EC%82%B4_%EC%B0%B8%EC%B9%98_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201005%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201005T154310Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=f0c4f8da699e7ecd743c25dab28b5089c41a14816ccd60243e12be438b29e9f7",
                    "sales": null,
                    "tagging": [],
                    "discount_price": null,
                    "sales_count": 98,
                    "stock": {
                        "id": 1178,
                        "count": 60,
                        "updated_at": "2020-08-19T18:04:36.022000Z"
                    }
                },
                ...(추가 상품 데이터)
            ]
        ```
        """
        qs = Goods.objects.filter(types__type__category__name='반려동물').order_by('-sales_count')[:10]
        serializers = self.get_serializer(qs, many=True)
        data = {
            "bool": True,
            "title": "반려동물 판매 랭킹",
            "serializers": serializers.data,
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False)
    def home_appliances(self, request):
        """
        추천 - 가전제품 판매 랭킹

        ----
        반려동물 랭킹과 동일
       """
        qs = Goods.objects.filter(types__type__category__name='가전제품').order_by('-sales_count')[:10]
        serializers = self.get_serializer(qs, many=True)
        data = {
            "bool": True,
            "title": "가전제품 판매 랭킹",
            "serializers": serializers.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False)
    def ice_cream(self, request):
        """
        추천 - 아이스크림 판매 랭킹

        ----
        반려동물 랭킹과 동일
       """
        qs = Goods.objects.filter(types__type__name='아이스크림').order_by('-sales_count')
        serializers = self.get_serializer(qs, many=True)
        data = {
            "bool": True,
            "title": "아이스크림 판매 랭킹",
            "serializers": serializers.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False)
    def salted_fish(self, request):
        """
        추천 - 밥상 위의 별미, 젓갈

        ---
        # 밥상 위의 별미, 젓갈 API
        """
        qs = Goods.objects.filter(title__icontains='젓')
        serializers = self.get_serializer(qs, many=True)
        data = {
            'bool': False,
            "title":"밥상 위의 별미, 젓갈",
            "serializers": serializers.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, )
    def chicken_goods(self, request):
        """
        추천 - 닭고기로 맛있는 식사 API

        ---
        # 닭고기로 맛있는 식사! API

        매 요청시 8개의 상품 랜덤 반환
        """
        lst = []
        qs_list = []
        list_length_limit = 8
        qs = Goods.objects.filter(title__icontains='닭')
        while True:
            random_pk = random.randint(0, qs.count() - 1)
            if random_pk in lst:
                continue
            elif random_pk == 0:
                continue
            else:
                lst.append(random_pk)
                qs_list.append(qs[random_pk])
            if len(lst) == list_length_limit:
                break
        serializer = self.get_serializer(qs_list, many=True)
        data = {
            "bool": False,
            "title":"닭고기로 맛있는 식사",
            "serializers": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False)
    def new_product(self, request):
        """
        홈 - 신상품 API

        ----
        홈 신상품 정렬 형식 다른 데이터들과 동일하며, 신상품은 최산 상품 50개까지만 반환 x됩니다.
        """
        qs = Goods.objects.order_by('-stock__updated_at')[:50]
        serializers = self.get_serializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, )
    def often_purchase_goods(self, request):
        """
        마이컬리 - 주문내역 - 자주사는 상품 API

        ---
        마이컬리 주문내역 - 자주사는 상품에 대한 API 이며

        각 serializers index 와 goods_purchase_count 의 index를 맞추면 해당 상품에 대한 구매 횟수가 됩니다.
        """
        qs = self.get_queryset().filter(items__order__user=request.user)
        goods_dict = defaultdict(int)
        for goods in qs:
            goods_dict[goods] += 1

        serializers = self.get_serializer([goods for goods, count in goods_dict.items()], many=True)
        data = {
            "serializers": serializers.data,
            "goods_purchase_count": [count for goods, count in goods_dict.items()]
        }
        return Response(data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers
    swagger_schema = MyAutoSchema

    def get_serializer_class(self):
        if self.action in ['md_recommend']:
            return CategoryGoodsSerializers
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        카테고리 요청 API

        -----
        예시

        ```
        [
            {
                "name": "채소",
                "category_img": "https://pbs-13-s3.s3.amazonaws.com/category_img/icon_veggies_active_pc2x.1586324570.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202047Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3659617eb9b4890eb12bb12a39622d9098f37d4b8ddd1bb3b4bb9fea1d03d7b6",
                "types": [
                    {
                        "name": "기본채소"
                    },
                    {
                        "name": "쌈·샐러드·간편채소"
                    },
                    {
                        "name": "브로콜리·특수채소"
                    },
                    {
                        "name": "콩나물·버섯류"
                    },
                    {
                        "name": "시금치·부추·나물"
                    },
                    {
                        "name": "양파·마늘·생강·파"
                    },
                    {
                        "name": "파프리카·피망·고추"
                    }
                ]
            },
            {
                "name": "과일·견과·쌀",
                "category_img": "https://pbs-13-s3.s3.amazonaws.com/category_img/icon_fruit_active_pc2x.1568684150.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202047Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=fc521a1cda46700c0eadbe691231a05fb64e2aef38d03aae1149892b65a6ffdd",
                "types": [
                    {
                        "name": "제철과일"
                    },
                    {
                        "name": "국산과일"
                    },
                    {
                        "name": "수입과일"
                    },
                    {
                        "name": "냉동·건과일"
                    },
                    {
                        "name": "견과류"
                    },
                    {
                        "name": "쌀·잡곡"
                    }
                ]
            },
            ....
        ]
        ```
        """
        return super().list(request, *args, **kwargs)

    @action(detail=False, )
    def md_recommend(self, request):
        """
        MD의 추천 API

        ---
        - 카테고리당 6개의 상품을 매 요청시 랜덤으로 응답합니다.
        """
        qs = self.get_queryset()
        serializers = self.get_serializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

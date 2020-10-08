from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.instructors import MyAutoSchema
from event.serializers import EventSerializers, MainEventSerializers, EventRetrieveSerializers, \
    MainEventRetrieveSerializers, EventImageSquareSerializers
from .models import Event, MainEvent


class EventAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['goods__price', 'goods__sales__discount_rate']
    swagger_schema = MyAutoSchema

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventRetrieveSerializers
        elif self.action == 'square_event_list':
            return EventImageSquareSerializers
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        홈 - 이벤트 리스트  API

        ---
        예제
        ```
        [
            {
                "id": 1,
                "title": "[모음전] 해물육수",
                "image": "https://pbs-13-s3.s3.amazonaws.com/event/seefood-collect.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T201239Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4279fc0a951786a2c4f232b5a89994ddc4b5a926cb9c27b5faefb6369ee6432a"
            },
            {
                "id": 2,
                "title": "[모음전] 오미자",
                "image": "https://pbs-13-s3.s3.amazonaws.com/event/schisandra.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T201239Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3f7e22aaca6a3c46ae8eabc7b60c431f26d43fe8aaa365bfaf4e712251a47ad2"
            },
            {
                "id": 3,
                "title": "[모음전] 키친타올",
                "image": "https://pbs-13-s3.s3.amazonaws.com/event/kitchen-towel.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T201239Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4c647c2b9f0394ac8b4ad843abd007a8110ac67c71e4fbb06b7d77e52a02fda8"
            },
            {
                "id": 4,
                "title": "[모음전] 뷰코",
                "image": "https://pbs-13-s3.s3.amazonaws.com/event/beako.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T201239Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=b4850eb40f0764781e3a655b793933d75e8bda9337546371a6e2d278d403e0ea"
            },
            {
                "id": 5,
                "title": "[모음전] 미당",
                "image": "https://pbs-13-s3.s3.amazonaws.com/event/midang.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T201239Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=957ff0f5350c99e6f5d18064cdb795c045c1073caf355961ad3d0d1b30246b5f"
            }
        ]
        ```
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        이벤트 상세 API

        ---
        배송 정보 goods > transfer # '샛별배송 ONLY' or '샛별배송/택배배송', or Null 입니다.

        상품 가격

        할인률이 있다면 goods > discount_price

        할인률이 없다면 goods > price

        할인률 goods > sales > discount_rate

        """
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, )
    def square_event_list(self, request):
        """
        홈 - 컬리추천 이벤트 API

        ---
        이미지가 4각형으로 나열 되는 api
        ```
        [
            {
                "id": 1,
                "title": "[모음전] 해물육수",
                "square_image": "https://pbs-13-s3.s3.amazonaws.com/event/square/seefood_broth.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201004%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201004T100743Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=8f511d211fb6bbfc1fb6af4f34c60f52283b55a1481f187269be6ed12637fe06",
                "goods": [
                    {
                        "id": 1217,
                        "title": "[바다원] 대관령 북어채 100g",
                        "short_desc": "반찬 걱정 덜어주는 구수한 감칠맛",
                        "packing_status": "냉장",
                        "transfer": "샛별배송/택배배송",
                        "price": 6715,
                        "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5B%EB%B0%94%EB%8B%A4%EC%9B%90%5D%20%EB%8C%80%EA%B4%80%EB%A0%B9%20%EB%B6%81%EC%96%B4%EC%B1%84%20100g/%EB%B0%94%EB%8B%A4%EC%9B%90_%EB%8C%80%EA%B4%80%EB%A0%B9_%EB%B6%81%EC%96%B4%EC%B1%84_100g_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201004%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201004T100744Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=a0c1b664a579290441f9a643e1b5dfd84219793ab709b7d6b4b1297c3e0f0b8e",
                        "sales": {
                            "discount_rate": null,
                            "contents": "1+1"
                        },
                        "tagging": [],
                        "discount_price": null,
                        "sales_count": 97,
                        "stock": {
                            "id": 1217,
                            "count": 32,
                            "updated_at": "2020-08-12T18:04:36.574000Z"
                        }
                    },
                    ...
                ]
                ...
            }
            ...
        ]
        ```
        """
        qs = self.get_queryset()
        serializers = self.get_serializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class MainEventAPIView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = MainEvent.objects.all()
    serializer_class = MainEventSerializers
    swagger_schema = MyAutoSchema

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MainEventRetrieveSerializers
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        컬리추천 - 최 상단 이벤트 페이지

        ---
        예시
        ```
        [
            {
                "id": 1,
                "title": "매콤달콤 우리집 식탁",
                "image": "https://pbs-13-s3.s3.amazonaws.com/mainEvent/list/spicy_sweet.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202443Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=f63a9e58ec13d3b2400fa042df1965fd862cd8724ef2f5f33b4ada7c8a9d45be"
            },
            {
                "id": 2,
                "title": "아이들 입맛 책임질 간편식",
                "image": "https://pbs-13-s3.s3.amazonaws.com/mainEvent/list/snack.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202443Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=2c8df3a07247ea14e5ed2375bebe9ce4f1319e09c6528a3e65e262a8c01a6eec"
            },
            {
                "id": 3,
                "title": "햅쌀로 즐기는 솥밥",
                "image": "https://pbs-13-s3.s3.amazonaws.com/mainEvent/list/rice.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202443Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=ab309fdf2ef536f1213f0bb5f82912675c0a0243c08ab8d07a930b266bcd3c73"
            },
            {
                "id": 4,
                "title": "달걀 레시피 기획전",
                "image": "https://pbs-13-s3.s3.amazonaws.com/mainEvent/list/egg.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20200930%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20200930T202443Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=09ae4cd4e6b4729425620381fd87fde4eb612fb76f2afcf791ecdcba504f5717"
            }
        ]
        ```
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        이벤트 상세

        ---
        배송 정보 event > mainEvent > goods > transfer

        상품 가격

        할인률이 있다면 event > mainEvent > goods > discount_price

        할인률이 없다면 event > mainEvent > goods > price

        상품 할인률 event > mainEvent > goods > sales > discount_rate
        """
        return super().retrieve(request, *args, **kwargs)

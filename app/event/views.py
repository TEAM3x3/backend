from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet

from core.instructors import MyAutoSchema
from event.serializers import EventSerializers, MainEventSerializers, EventRetrieveSerializers, \
    MainEventRetrieveSerializers
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

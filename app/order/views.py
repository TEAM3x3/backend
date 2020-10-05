import requests
from django.db import transaction
from django.db.models import F
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.instructors import MyAutoSchema
from goods.models import Goods
from order.models import Order, OrderReview, OrderDetail
from order.permissions import OrderReviewPermission, OrderPermission
from order.serializers import OrderCreateSerializers, ReviewUpdateSerializers, OrderSerializers, \
    OrderDetailCreateSerializers, ReviewListSerializers, ReviewCreateSerializers


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
                return self.queryset.filter(user_id=self.kwargs['user_pk'])
        except KeyError:
            return super().get_queryset()

    @action(detail=True, methods=['POST'])
    def payment(self, request, pk):
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "f9f70eb192ef14919735fb40a6e599f5",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        try:
            order_ins = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            order_ins = None

        if order_ins:
            cart_ins = order_ins.items.first().cart

            params = {
                "cid": "TC0ONETIME",  # 테스트용 코드
                "partner_order_id": f'{order_ins.id}',  # 주문번호
                "partner_user_id": f'{self.request.user.username}',  # 유저 아이디
                "item_name": f'{request.user}의 상품 구매',  # 구매 물품 이름
                "quantity": f'{cart_ins.quantity_of_goods}',  # 구매 물품 수량
                "total_amount": f'{order_ins.discount_payment}',  # 구매 물품 가격
                "tax_free_amount": "0",  # 구매 물품 비과세
                "approval_url": f"http://localhost:8000/api/order/{order_ins.id}/approve",
                "cancel_url": "https://developers.kakao.com/fail",
                "fail_url": "https://developers.kakao.com/cancel",
            }
            del request.session['partner_order_id']
            del request.session['partner_user_id']
            del request.session['tid']
            request.session.modified = True

            response = requests.post(URL, headers=headers, params=params)
            request.session['tid'] = response.json()['tid']  # 결제 고유 번호, 20자 결제 승인시 사용할 tid를 세션에 저장
            request.session['partner_order_id'] = order_ins.id
            request.session['partner_user_id'] = self.request.user.username
            next_url = response.json()['next_redirect_pc_url']  # 카카오톡 결제 페이지 Redirect URL
            return Response({"next": f"{next_url}"}, status=status.HTTP_200_OK)

        data = {
            "message": "존재하지 않은 Order PK 입니다."
        }
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

    @transaction.atomic
    @action(detail=True, methods=['get', 'post'])
    def approve(self, request, *args, **kwargs):
        """
        * html로 테스트를 하는 이유는 API로 하면 세션에 값이 저장이 되지를 않습니다. --> 구글링을 통해 세션에 대한 학습 중, 아직 원인을 찾지 못하고 있습니다.
        * 원인 추론 // 설마 'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication',] ?? 결과 X
        * html로 요청 할 때에만 tid가 올바르게 들어간다.
        질문 : 'html 카카오페이 결제 클릭' -> '카카오페이 서버의 결제 페이지' -> '성공 시 redirect url' 의 순서로 카카오페이 결제가 진행이 되고 있습니다.
        구현 과정 중 'html 카카오페이 결제 클릭' 의 view에서
        '성공 시 redirect url' 의 view 에서 사용을 해야 하는 값들을 세션을 통하여 넘겨주고 있습니다.
        ios와 통신할 때에는 제가 필요한 값들을 어떻게 의사소통을 해야 할까요??
        ios에서 세션을 통해 값을 넘겨 주는지 아직 ios가 결제 기능을 구현하지 않아서 제가 세션 말고 다른 준비해야 하는 부분이 있는지 궁금합니다.

        * view에는 로직이 들어가면 좋지 않은데 결제 정보를 디비에 넣는 형식으로 해서 serializers 를 만들고,
        serializers에 views에서 작성하였던 코드를 넣는게 올바른 방식인지 질문드립니다. >> 아니면 payment.py를 만들고 거기서 함수를 호출하는 형식으로 할까요?
        """
        try:
            order_ins = Order.objects.get(pk=kwargs['pk'])
        except Order.DoesNotExist:
            order_ins = None
        if order_ins:
            # 카카오 페이 승인 통신
            URL = 'https://kapi.kakao.com/v1/payment/approve'
            headers = {
                "Authorization": "KakaoAK " + "f9f70eb192ef14919735fb40a6e599f5",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            }
            params = {
                "cid": "TC0ONETIME",  # 테스트용 코드
                "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
                "partner_order_id": request.session['partner_order_id'],  # 주문번호
                "partner_user_id": request.session['partner_user_id'],  # 유저 아이디
                "pg_token": request.GET.get("pg_token"),  # 쿼리 스트링으로 받은 pg토큰
            }
            response = requests.post(URL, headers=headers, params=params)
            if response.status_code == 200:
                order_ins = Order.objects.get(pk=request.session['partner_order_id'])
                for item in order_ins.items.all():
                    item.cart = None

                    item.goods.sales_count = F('sales_count') + 1
                    stock = item.goods.stock
                    stock.count = F('count') - 1

                    item.save()
                    item.goods.save()
                    stock.save()

                response = response.json()
                amount = response['amount']['total']
                context = {
                    'res': response,
                    'amount': amount,
                }
                del request.session['partner_order_id']
                del request.session['partner_user_id']
                del request.session['tid']
                request.session.modified = True

                return Response(data=context, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(mixins.CreateModelMixin, GenericViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailCreateSerializers

    def perform_create(self, serializer):
        order_instance = Order.objects.get(pk=self.kwargs['order_pk'])
        serializer.save(order=order_instance)


class ReviewAPI(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = OrderReview.objects.all()
    serializer_class = ReviewCreateSerializers
    swagger_schema = MyAutoSchema

    """
    배송이 완료 되기 전 'r' ready
    배송 완료- 후기 작성 가능 상태 'p' possible
    후기 작성 완료 'd' done 
    """

    def get_queryset(self):
        try:
            goods_pk = self.kwargs['goods_pk']
            if goods_pk:
                return self.queryset.filter(goods_id=goods_pk)
        except KeyError:
            return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['partial_update']:
            return ReviewUpdateSerializers
        elif self.action in ['list', 'retrieve']:
            return ReviewListSerializers
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [OrderReviewPermission(), ]
        # 참고 링크 :https://stackoverflow.com/questions/35970970/django-rest-framework-permission-classes-of-viewset-method
        return [permissions() for permissions in self.permission_classes]

    def list(self, request, *args, **kwargs):
        """
        후기 list api

        ----
        # /api/review 와 /api/goods/{goods_pk}/reviews 에 대한 요청의 응답 값은 다릅니다.

        1. /api/review는 토큰이 헤더에 포함이 되어야 하며, 토큰에 해당하는 유저가 작성한 리뷰 리스트를 반환합니다.
        ```
        [
            {
                "id": 1,
                "user": {
                    "username": "admin"
                },
                "created_at": "2020-09-23T14:27:56.192000Z",
                "title": "update review title",
                "content": "update review content",
                "goods": {
                    "id": 1,
                    "title": "[KF365] 햇 감자 1kg",
                    "short_desc": "믿고 먹을 수 있는 상품을 합리적인 가격에, KF365",
                    "packing_status": "상온",
                    "transfer": "샛별배송/택배배송",
                    "price": 2380,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKF365%5D%20%ED%96%87%20%EA%B0%90%EC%9E%90%201kg/KF365_%ED%96%87_%EA%B0%90%EC%9E%90_1kg_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T170201Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=d5f34d0eecafc0a29eed7e2cda0018232ea609ee1f6c8c194188024c6c4b012f",
                    "sales": null,
                    "tagging": [],
                    "discount_price": null,
                    "sales_count": 6,
                    "stock": {
                        "id": 1,
                        "count": 82,
                        "updated_at": "2020-08-18T18:05:16.687000Z"
                    }
                }
            },
            {
                "id": 2,
                "user": {
                    "username": "user0"
                },
                "created_at": "2020-10-05T12:31:05.851348Z",
                "title": "title exam",
                "content": "content exam",
                "goods": {
                    "id": 2,
                    "title": "한끼 당근 1개",
                    "short_desc": "딱 하나만 필요할 때 한끼 당근",
                    "packing_status": "냉장",
                    "transfer": "샛별배송/택배배송",
                    "price": 1000,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%ED%95%9C%EB%81%BC%20%EB%8B%B9%EA%B7%BC%201%EA%B0%9C/%ED%95%9C%EB%81%BC_%EB%8B%B9%EA%B7%BC_1%EA%B0%9C_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T170201Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=87bfa3347b159a2086d20405b69a249591a573e5addf1552e01b1a294644baf4",
                    "sales": {
                        "discount_rate": 30,
                        "contents": null
                    },
                    "tagging": [],
                    "discount_price": 700,
                    "sales_count": 68,
                    "stock": {
                        "id": 2,
                        "count": 27,
                        "updated_at": "2020-09-17T18:04:43.110000Z"
                    }
                }
            }
        ]
        ```

        2. /api/goods/{goods_pk}/reviews는 해당 상품에 대한 리뷰를 리스트 형태로 반환합니다.
        ```
        [
            {
                "id": 1,
                "user": {
                    "username": "user0"
                },
                "created_at": "2020-10-05T12:31:05.851348Z",
                "title": "update review title",
                "content": "update review content",
                "goods": {
                    "id": 1,
                    "title": "[KF365] 햇 감자 1kg",
                    "short_desc": "믿고 먹을 수 있는 상품을 합리적인 가격에, KF365",
                    "packing_status": "상온",
                    "transfer": "샛별배송/택배배송",
                    "price": 2380,
                    "img": "https://pbs-13-s3.s3.amazonaws.com/goods/%5BKF365%5D%20%ED%96%87%20%EA%B0%90%EC%9E%90%201kg/KF365_%ED%96%87_%EA%B0%90%EC%9E%90_1kg_goods_image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXOLZAM2NBPACFGX7%2F20201001%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20201001T170100Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=0c4b1b2e065fb510c9e420c24e7cdcd003761f2244352710ef229d3e496fa3b7",
                    "sales": null,
                    "tagging": [],
                    "discount_price": null,
                    "sales_count": 6,
                    "stock": {
                        "id": 1,
                        "count": 82,
                        "updated_at": "2020-08-18T18:05:16.687000Z"
                    }
                }
            }
            ...
        ]
        ```

        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        후기 생성

        ----
        토큰이 필요한 요청입니다.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        리뷰 상세 요청

        ---

        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        사용하지 않을 api 입니다.

        ----
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        후기 업데이트

        ---
        title, content 만 수정하며, 토큰이 필요합니다.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        후기 삭제

        ---
        토큰이 필요한 요청 입니다.
        """
        return super().destroy(request, *args, **kwargs)

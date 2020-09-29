import requests
from django.db import transaction
from django.db.models import F
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from order.models import Order, OrderReview, OrderDetail
from order.permissions import OrderReviewPermission, OrderPermission
from order.serializers import OrderCreateSerializers, ReviewSerializers, \
    ReviewUpdateSerializers, OrderSerializers, OrderDetailCreateSerializers


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
    serializer_class = ReviewSerializers
    """
    배송이 완료 되기 전 'r' ready
    배송 완료- 후기 작성 가능 상태 'p' possible
    후기 작성 완료 'd' done 
    """

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            goods_pk = self.kwargs['goods_pk']
            if goods_pk:
                return self.queryset.filter(goods_id=goods_pk)
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ['partial_update']:
            return ReviewUpdateSerializers
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [OrderReviewPermission(), ]
        # 참고 링크 :https://stackoverflow.com/questions/35970970/django-rest-framework-permission-classes-of-viewset-method
        return [permissions() for permissions in self.permission_classes]
9
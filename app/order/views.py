import requests
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from order.models import Order, OrderReview, OrderDetail
from order.permissions import OrderReviewPermission, OrderPermission
from order.serializers import OrderCreateSerializers, ReviewSerializers, \
    ReviewUpdateSerializers, OrderSerializers, OrderDetailSerializers


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
                return self.queryset.filter(user_id=self.kwargs['user_pk']).filter(orderdetail__status='배송완료')
        except KeyError:
            return super().get_queryset()

    @action(detail=True, methods=['POST'])
    def payment(self, request, pk):
        """
         payment 데이터 생성? 아니면 order Detail instance data update?
         --> 이유 : view안에 논리적인 코드가 있는건 이상하고, 결제에 대한 데이터가 있어야 한다면 디비에 저장이 되어야 하니까
        """
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
            del request.session['partner_user_id']
            del request.session['partner_order_id']
            request.session.modified = True

            res = requests.post(URL, headers=headers, params=params)
            request.session['tid'] = res.json()['tid']  # 결제 고유 번호, 20자 결제 승인시 사용할 tid를 세션에 저장
            request.session['partner_order_id'] = order_ins.id
            request.session['partner_user_id'] = self.request.user.username
            next_url = res.json()['next_redirect_pc_url']  # 카카오톡 결제 페이지 Redirect URL

            return Response({"next": f"{next_url}"}, status=status.HTTP_200_OK)

        data = {
            "message": "존재하지 않은 Order PK 입니다."
        }
        return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

    @action(detail=True, methods=['get', 'post'])
    def approve(self, request, *args, **kwargs):
        # 질문 : kakao pay에서 redirect로 올 때에는 세션에 tid만 담겨 나오지만,
        # localhost에서는 둘 다 나옵니다. 카카오페이 서버에서 결제 완료 후 session에 값을 주입하는 과정에서 제가 실수한 부분이 무엇일까요?
        print('approve')
        print(request.session['tid'])
        print(request.session['partner_order_id'])
        print(request.session['partner_user_id'])
        try:
            order_ins = Order.objects.get(pk=kwargs['pk'])
        except Order.DoesNotExist:
            order_ins = None
        if order_ins:
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
            res = requests.post(URL, headers=headers, params=params)
            amount = res.json()['amount']['total']
            res = res.json()
            context = {
                'res': res,
                'amount': amount,
            }
            return Response(data=context, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializers


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

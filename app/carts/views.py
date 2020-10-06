from django.contrib.auth import get_user_model
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from carts.models import CartItem, Cart
from carts.permissions import CartIsOwnerOrReadOnly, CartItemIsOwnerOrReadOnly
from carts.serializers import CartSerializer, CartItemCreateSerializer, CartItemSerializer
from core.instructors import MyAutoSchema

User = get_user_model()


class CartItemViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """
    해당 요청은 토큰이 필요합니다.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (CartItemIsOwnerOrReadOnly,)
    swagger_schema = MyAutoSchema

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemCreateSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.cart)

    def list(self, request, *args, **kwargs):
        """
        카트 아이템 나열

        ----

        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        장바구니 아이템 추가

        ----
        토큰이 반드시 필요합니다. 예제가 포함되어 있습니다.

        기존에 상품이 추가되어 있다면 400대 에러가 발생하며 에러 내용은

        "non_field_errors": ["already exists instanace."] 입니다.
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        해당 API는 사용하지 않습니다.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        장바구니 상품 업데이트

        ---

        토큰이 필요합니다.

        해당 상품에는 quantity 필드만 요청 부탁드립니다. 예제 >> {"quantity":"10"}
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        상품 삭제

        -----
        토큰이 필요합니다.

        """
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['delete'])
    def goods_delete(self, request, *args, **kwargs):
        """
        상품 다중 삭제

        ----
        삭제를 하려는 상품의 pk를 ,(컴마)를 사용하여 pk를 구분하여 전달해 주시면 됩니다.

        예시 >> {"items":"9,8"} 성공 status는 204 입니다.
        """
        req_goods = request.data.get('items')
        req_goods = req_goods.split(',')
        pk_list = []
        for char in req_goods:
            pk_list.append(int(char))

        goods_ins = CartItem.objects.filter(id__in=list(req_goods))

        for ins in goods_ins:
            ins.delete()
        return Response("clear", status=status.HTTP_204_NO_CONTENT)


class CartViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (CartIsOwnerOrReadOnly,)
    swagger_schema = MyAutoSchema

    def retrieve(self, request, *args, **kwargs):
        """
        카트 조회 - id는 user id와 동일

        ---
        """
        return super().retrieve(request, *args, **kwargs)

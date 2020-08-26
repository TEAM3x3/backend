from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from cart.views import CartViewSet, CartItemViewSet
from goods.views import GoodsViewSet
from members.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('goods', GoodsViewSet)
router.register('cart', CartViewSet)
router.register('cartitem', CartItemViewSet)

users_router = routers.NestedSimpleRouter(router, 'users')
goods_router = routers.NestedSimpleRouter(router, 'goods')
cart_router = routers.NestedSimpleRouter(router, 'cart')

urlpatterns = (
    url('', include(router.urls)),
)

from django.conf.urls import url
from django.urls import include, path
from rest_framework_nested import routers

from carts.views import CartItemViewSet, CartViewSet
from goods.views import GoodsViewSet, DeliveryViewSet, CategoryViewSet

from members.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('goods', GoodsViewSet)
router.register('carts', CartItemViewSet)
router.register('cart', CartViewSet)

router.register('delivery', DeliveryViewSet)
router.register('category', CategoryViewSet)

users_router = routers.NestedSimpleRouter(router, 'users')
goods_router = routers.NestedSimpleRouter(router, 'goods')
carts_router = routers.NestedSimpleRouter(router, 'carts')

urlpatterns = (
    url('', include(router.urls)),
)

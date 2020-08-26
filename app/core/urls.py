from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from carts.views import CartViewSet
from goods.views import GoodsViewSet
from members.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('goods', GoodsViewSet)
router.register('carts', CartViewSet)


users_router = routers.NestedSimpleRouter(router, 'users')
goods_router = routers.NestedSimpleRouter(router, 'goods')
carts_router = routers.NestedSimpleRouter(router, 'carts')

urlpatterns = (
    url('', include(router.urls)),
)

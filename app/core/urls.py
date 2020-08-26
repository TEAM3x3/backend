from django.conf.urls import url
from django.urls import include, path
from rest_framework_nested import routers

from goods.views import GoodsViewSet, DeliveryViewSet
from members.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('goods', GoodsViewSet)
router.register('delivery', DeliveryViewSet)

users_router = routers.NestedSimpleRouter(router, 'users')
goods_router = routers.NestedSimpleRouter(router, 'goods')

urlpatterns = (
    url('', include(router.urls)),
)

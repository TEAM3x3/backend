from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers

from carts.views import CartViewSet, CartItemViewSet
from event.views import EventAPIView
from goods.views import GoodsViewSet, DeliveryViewSet, CategoryViewSet

from members.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('goods', GoodsViewSet)
router.register('cart', CartViewSet)
router.register('delivery', DeliveryViewSet)
router.register('category', CategoryViewSet)
router.register('event', EventAPIView)

# /users
users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
# /goods
goods_router = routers.NestedSimpleRouter(router, 'goods', lookup='goods')
# /cart
cart_router = routers.NestedSimpleRouter(router, 'cart', lookup='cart')
cart_router.register('item', CartItemViewSet)

urlpatterns = (
    url('', include(router.urls)),
    url('', include(cart_router.urls)),
)

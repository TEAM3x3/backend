from django.conf.urls import url
from django.urls import include, path
from rest_framework_nested import routers
from carts.views import CartViewSet, CartItemViewSet
from event.views import EventAPIView, MainEventAPIView
from goods.views import GoodsViewSet, DeliveryViewSet, CategoryViewSet

from members.views import UserViewSet, UserAddressViewSet, UserSearchViewSet
from order.views import OrderView, ReviewAPI


router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('goods', GoodsViewSet)
router.register('cart', CartViewSet)
router.register('delivery', DeliveryViewSet)
router.register('category', CategoryViewSet)
router.register('event', EventAPIView)
router.register('order', OrderView)
router.register('address', UserAddressViewSet)
router.register('mainEvent', MainEventAPIView)
router.register('review', ReviewAPI)

# /users
users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
users_router.register('address', UserAddressViewSet)
users_router.register('orders', OrderView)
users_router.register('searchword', UserSearchViewSet)

# /goods
goods_router = routers.NestedSimpleRouter(router, 'goods', lookup='goods')

# goods_router.register('review', ReviewAPI)

# /cart
cart_router = routers.NestedSimpleRouter(router, 'cart', lookup='cart')
cart_router.register('item', CartItemViewSet)
# /address

address_router = routers.NestedSimpleRouter(router, 'address', lookup='address')

urlpatterns = router.urls + users_router.urls + goods_router.urls + cart_router.urls

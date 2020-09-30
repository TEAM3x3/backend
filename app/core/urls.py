from rest_framework_nested import routers
from carts.views import CartViewSet, CartItemViewSet
from event.views import EventAPIView, MainEventAPIView
from goods.views import GoodsViewSet, CategoryViewSet

from members.views import UserViewSet, UserAddressViewSet, UserSearchViewSet
from order.views import OrderView, ReviewAPI, OrderDetailView

router = routers.SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
router.register('goods', GoodsViewSet)
router.register('cart', CartViewSet)
router.register('category', CategoryViewSet)
router.register('event', EventAPIView)
router.register('order', OrderView)
router.register('mainEvent', MainEventAPIView)
router.register('review', ReviewAPI)

# / users
users_router = routers.NestedSimpleRouter(router, 'users', lookup='user')
users_router.register('address', UserAddressViewSet)
users_router.register('orders', OrderView)
users_router.register('search_word', UserSearchViewSet)

# /goods
goods_router = routers.NestedSimpleRouter(router, 'goods', lookup='goods')
goods_router.register('reviews', ReviewAPI)

# /cart
cart_router = routers.NestedSimpleRouter(router, 'cart', lookup='cart')
cart_router.register('item', CartItemViewSet)

# /order
order_router = routers.NestedSimpleRouter(router, 'order', lookup='order')
order_router.register('detail', OrderDetailView)

urlpatterns = router.urls + users_router.urls + goods_router.urls + cart_router.urls + order_router.urls

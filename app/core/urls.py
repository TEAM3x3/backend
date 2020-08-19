from django.conf.urls import url
from django.urls import include
from rest_framework_nested import routers
from members.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)

users_router = routers.NestedSimpleRouter(router, r'users', trailing_slash=False)


urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
)

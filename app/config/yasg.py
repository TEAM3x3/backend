from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="mackurly API",
        default_version='v1',
        description="http://13.209.33.72/ **Response Samples 에서 일부 'null'이라고 표현되는 값들은 예시 작성 중 파이썬 문법상의 문제이며, 정상적인 null 표기는 작은 따옴표가 없습니다.**",
        terms_of_service="http://13.209.33.72/",
        contact=openapi.Contact(email="hungyb0924@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns_yasg = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

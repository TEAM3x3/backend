import django_filters

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    transfer = django_filters.CharFilter(field_name='transfer', lookup_expr='contains')
    category = django_filters.CharFilter(field_name='types__type__category__name', lookup_expr='contains')
    type = django_filters.CharFilter(field_name='types__type__name', lookup_expr='contains')

    class Meta:
        model = Goods
        fields = ('transfer', 'category', 'type')

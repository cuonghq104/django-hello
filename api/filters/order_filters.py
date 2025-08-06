import django_filters

from api.models import Order


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Order
        fields = {
            'created_at': ['gt', 'lt', 'gte', 'lte', 'exact'],
        }
import django_filters

from api.models import Product
from rest_framework import filters

class ProductFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='istartswith')
    super_category = django_filters.NumberFilter(field_name='category__super_category', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'category', 'super_category']


class ProductInStockFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)
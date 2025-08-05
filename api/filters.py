import django_filters

from api.models import Product


class ProductFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Product
        fields = ['name']

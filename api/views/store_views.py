from django.db.models import Count
from rest_framework import viewsets

from api.models import Store
from api.serializers import StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.annotate(products_count=Count('products'))
    serializer_class = StoreSerializer
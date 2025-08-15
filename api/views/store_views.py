from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.models import Store
from api.permissions.store_permissions import IsStoreOwner
from api.serializers import StoreSerializer, StoreCreateSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.annotate(products_count=Count('products'))
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'delete':
            self.permission_classes = [IsAdminUser]
        elif self.action == 'update':
            self.permission_classes = [IsAdminUser, IsStoreOwner]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return StoreCreateSerializer
        return super().get_serializer_class()

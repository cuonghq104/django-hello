from xmlrpc.client import Fault

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.filters.order_filters import OrderFilter
from api.models import Order
from api.serializers import OrderSerializer, OrderCreateSerializer


# class OrderListApiView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('order_items__product').all()
#     serializer_class = OrderSerializer
#
#
# class UserOrderListApiView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('order_items__product').all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('order_items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(status=Order.StatusChoice.PENDING, user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='user-orders')
    def get_user_orders(self, request, pk=None):
        qs = self.get_queryset().filter(user=self.request.user)
        data = self.get_serializer(qs, many=True)
        return Response(data.data)

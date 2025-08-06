from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.filters.order_filters import OrderFilter
from api.models import Order
from api.serializers import OrderSerializer


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

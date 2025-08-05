from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import ProductFilter
from api.models import Product, Order, ProductCategory
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, \
    ProductSerializerWithCategoryAsObject, ProductCategorySerializer


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            self.serializer_class = ProductSerializerWithCategoryAsObject
        return super().get_serializer_class()


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            self.serializer_class = ProductSerializerWithCategoryAsObject
        return super().get_serializer_class()


class OrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('order_items__product').all()
    serializer_class = OrderSerializer


class UserOrderListApiView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('order_items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(serializer.data)


class ProductCategoryCreateListApiView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'category_id'

    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductByCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        category_id = kwargs.get('category_id')
        
        # Start with category filter
        queryset = Product.objects.filter(category_id=category_id)
        
        # Apply ProductFilter directly
        filterset = ProductFilter(request.query_params, queryset=queryset)
        filtered_queryset = filterset.qs

        serializer = ProductSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

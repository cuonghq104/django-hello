from django.db.models import Max
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import ProductFilter, ProductInStockFilter
from api.models import Product
from api.serializers import ProductSerializer, ProductSerializerWithCategoryAsObject, ProductInfoSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, ProductInStockFilter]

    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.max_page_size = 6
    pagination_class.page_size_query_param = 'page_size'
    pagination_class.page_query_param = 'page_num'

    permission_classes = [AllowAny]
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            self.serializer_class = ProductSerializerWithCategoryAsObject
        return super().get_serializer_class()

    def filter_queryset(self, queryset):
        # Get query parameters
        super_category = self.request.query_params.get('super_category')
        category = self.request.query_params.get('category')
        
        # If both super_category and category are provided, ignore category
        if super_category and category:
            # Create a copy of query params and remove category
            query_params = self.request.query_params.copy()
            query_params.pop('category', None)
            
            # Apply filters manually with modified query params
            filterset = self.filterset_class(query_params, queryset=queryset)
            return filterset.qs
        
        # Otherwise, use the default filtering
        return super().filter_queryset(queryset)


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


class ProductInfoApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(serializer.data)
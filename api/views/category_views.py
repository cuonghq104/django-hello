from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.models import ProductCategory, ProductSuperCategory
from api.serializers import ProductCategorySerializer, ProductSuperCategorySerializer


class ProductSuperCategoryCreateListApiView(generics.ListCreateAPIView):
    queryset = ProductSuperCategory.objects.all()
    serializer_class = ProductSuperCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductSuperCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductSuperCategory.objects.all()
    serializer_class = ProductSuperCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductCategoryCreateListApiView(generics.CreateAPIView):
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

from decimal import Decimal

from rest_framework import serializers

from api.models import Product
from .store_serializers import StoreSimpleSerializer
from .category_serializers import ProductCategorySerializer


class ProductSerializerRoot(serializers.ModelSerializer):
    discount_price = serializers.SerializerMethodField(read_only=True)
    def get_discount_price(self, obj):
        return obj.price * (Decimal(100 - obj.discount_percentage) / Decimal(100))


class ProductSerializerWithCategoryAsObject(ProductSerializerRoot):
    category = ProductCategorySerializer(many=False)
    store = StoreSimpleSerializer(many=False)
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category',
            'discount_percentage',
            'discount_price',
            'store'
        )


class ProductSerializer(ProductSerializerRoot):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category',
            'discount_percentage',
            'discount_price',
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Price must be greater than 0"
            )
        return value


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()

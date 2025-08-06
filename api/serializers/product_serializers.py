from rest_framework import serializers

from api.models import Product
from .category_serializers import ProductCategorySerializer


class ProductSerializerWithCategoryAsObject(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category'
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category'
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

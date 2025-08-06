from rest_framework import serializers

from api.models import ProductCategory, ProductSuperCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'name'
        )


class ProductSuperCategorySerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, read_only=True)
    class Meta:
        model = ProductSuperCategory
        fields = '__all__'

from rest_framework import serializers

from api.models import Store


class StoreSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'location'
        )


class StoreSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Store
        fields = '__all__'

    # Note: To use this serializer efficiently, in your view you should use:
    # stores = Store.objects.annotate(products_count=Count('products'))
    # This will perform the count in a single SQL query instead of N+1 queries

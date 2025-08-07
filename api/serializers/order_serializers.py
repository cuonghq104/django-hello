from django.db import transaction
from rest_framework import serializers

from api.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'product_name',
            'product_price',
            'item_subtotal'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = (
                'product',
                'quantity',
            )

    order_id = serializers.UUIDField(read_only=True)
    order_items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'user',
            'order_items'
        )
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in order_items:
                OrderItem.objects.create(order=order, **item)

        return order

    def update(self, instance, validated_data):
        order_items = validated_data.pop('order_items')
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if order_items is not None:
                instance.order_items.all().delete()

                for item in order_items:
                    OrderItem.objects.create(order=instance, **item)

            return instance


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.order_items.all()
        return sum(item.item_subtotal for item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'order_items',
            'total_price'
        )

from django.db import transaction
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from api.models import Store, StoreStaff, User
from .base_serializers import BaseSerializer
import os

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


class StoreStaffLoginSerializer(serializers.ModelSerializer):
    store = StoreSimpleSerializer(read_only=True)
    class Meta:
        model = StoreStaff
        fields = (
            'store',
            'role'
        )

class StoreStaffCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = StoreStaff
        fields = (
            'user',
            'role'
        )


class StoreCreateSerializer(BaseSerializer):
    staff_users = StoreStaffCreateSerializer(many=True)

    class Meta:
        model = Store
        fields = (
            'name',
            'location',
            'description',
            'staff_users'
        )

    def create(self, validated_data):
        staff_users = validated_data.pop('staff_users')
        current_user = self.get_current_user()
        print(current_user)
        with transaction.atomic():
            store = Store.objects.create(**validated_data)
            if not staff_users:
                StoreStaff.objects.create(store=store, user=current_user, role="1")
            else:
                for staff_data in staff_users:
                    # staff_data now contains validated data with user as User instance
                    user_instance = staff_data.get('user')
                    if user_instance.id != current_user.id:
                        print(current_user)
                        StoreStaff.objects.create(store=store, user=user_instance, role=staff_data.get('role', '2'))
                    else:
                        print(current_user)
                        StoreStaff.objects.create(store=store, user=current_user, role="1")
        return store


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid Request',
            value={
                'id': 1,
                'file': 'file.csv'
            },
            request_only=True,
            media_type='multipart/form-data'
        )
    ]
)
class StoreProductBulkCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        help_text="Store ID where products will be created",
        min_value=1
    )
    file = serializers.FileField(
        help_text="File to upload (CSV, Excel, etc.)",
        allow_empty_file=False,
        use_url=False
    )

    def validate_file(self, file):
        ext = os.path.splitext(file.name)[1].lower()
        if ext != ".csv":
            raise serializers.ValidationError("Only CSV files are allowed.")
        return file
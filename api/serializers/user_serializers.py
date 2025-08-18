from rest_framework import serializers

from api.models import User
from .store_serializers import StoreStaffLoginSerializer
from api.validators import load_validators


class UserSerializer(serializers.ModelSerializer):
    managed_stores = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'managed_stores')
        extra_kwargs = {'is_active': {'read_only': True}, 'managed_stores': {'read_only': True}}

    def get_managed_stores(self, obj):
        active_stores = obj.managed_stores.filter(is_active=True)
        return StoreStaffLoginSerializer(active_stores, many=True).data


class UserSerializerAdmin(serializers.ModelSerializer):
    model = User
    fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=load_validators('AUTH_CUSTOM_PASSWORD_VALIDATORS'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=load_validators('AUTH_CUSTOM_PASSWORD_VALIDATORS'))

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

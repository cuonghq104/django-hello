from rest_framework import serializers

from api.models import User
from api.validators import load_validators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
        extra_kwargs = {'is_active': {'read_only': True}}


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

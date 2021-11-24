from drf_spectacular.utils import extend_schema

from rest_framework import serializers, status

from rest_framework_simplejwt import views


class TokenObtainRequestSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class TokenObtainResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class TokenVerifyRequestSerializer(serializers.Serializer):
    token = serializers.CharField()


class TokenVerifyResponseSerializer(serializers.Serializer):
    pass
from drf_spectacular.utils import extend_schema

from rest_framework import serializers, status

from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt import views


class TokenObtainRequestSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class TokenObtainResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenObtainPairView(views.TokenObtainPairView):
    @extend_schema(
        request=TokenObtainRequestSerializer,
        responses={
            status.HTTP_200_OK: TokenObtainResponseSerializer
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class TokenRefreshView(views.TokenRefreshView):
    @extend_schema(
        request=TokenRefreshRequestSerializer,
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(views.TokenVerifyView):
    @extend_schema(
        request=TokenVerifySerializer,
        responses={
            status.HTTP_200_OK: None
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

from drf_spectacular.utils import extend_schema

from rest_framework import serializers, status
from rest_framework_simplejwt import views

from account import serializers
from api.serializers import ErrorDescriptionSerializer

class TokenObtainPairView(views.TokenObtainPairView):
    @extend_schema(
        request=serializers.TokenObtainRequestSerializer,
        responses={
            status.HTTP_200_OK: serializers.TokenObtainResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: None
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(views.TokenRefreshView):
    @extend_schema(
        request=serializers.TokenRefreshRequestSerializer,
        responses={
            status.HTTP_200_OK: serializers.TokenRefreshResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ErrorDescriptionSerializer
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(views.TokenVerifyView):
    @extend_schema(
        request=serializers.TokenVerifyRequestSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: ErrorDescriptionSerializer
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

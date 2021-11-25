from django.contrib.auth import login as auth_login
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, generics, status
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response

from rest_framework_simplejwt import views
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from account import models as accounts
from account import serializers
from api.serializers import ErrorDescriptionSerializer

class TokenObtainPairView(views.TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    @extend_schema(
        request=serializers.TokenObtainRequestSerializer,
        responses={
            status.HTTP_200_OK: serializers.TokenObtainResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: None
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(views.TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    @extend_schema(
        request=serializers.TokenRefreshRequestSerializer,
        responses={
            status.HTTP_200_OK: serializers.TokenRefreshResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ErrorDescriptionSerializer
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(views.TokenVerifyView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    @extend_schema(
        request=serializers.TokenVerifyRequestSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: ErrorDescriptionSerializer
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GoogleAuthView(views.TokenViewBase):
    serializer_class = serializers.GoogleIdTokenSerializer

    @extend_schema(
        request=serializers.GoogleIdTokenSerializer,
        responses={
            status.HTTP_200_OK: serializers.TokenObtainResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ErrorDescriptionSerializer,
            status.HTTP_401_UNAUTHORIZED: ErrorDescriptionSerializer,
        })
    def post(self, request, *args, **kwargs):
        """
        Takes a Google ID token and returns an access and refresh token for this API.
        If token is valid and user does not already exist, a new Genie user will be created.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        google_id = serializer.validated_data
        user = self.get_user(google_id)

        # Authorize User for Admin access
        auth_login(self.request, user)
        token = RefreshToken.for_user(user)

        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=status.HTTP_200_OK)

    def get_user(self, google_id):
        """
        Search user by verified Google email address
        """
        try:
            return accounts.User.objects.get(email=google_id['email'])
        except accounts.User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials provided.')
        except KeyError:
            raise ValidationError('Email address is required.')


class PasswordResetView(generics.GenericAPIView):
    """
    Request password reset. Send an email to the user first.
    """
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'detail': _('Password reset e-mail has been sent.')
        })


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Password reset e-mail link is confirmed, reset the user's password.
    """
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = []
    authentication_classes = []

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'detail': _('Password has been reset with the new password.')
        })
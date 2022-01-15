from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests

from account import models as accounts


class TokenClaimsSerializer(TokenObtainPairSerializer):
    """
    Append custom claims to JWT Token
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Unique and verified email address
        token['email'] = user.email

        # Simple user display name
        token['name'] = user.display_name

        return token

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


class GoogleIdTokenSerializer(serializers.Serializer):
    """
    Verify Google ID Token and ensure email is verified
    """

    token = serializers.CharField()

    def validate(self, attrs):
        try:
            client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
            google_id = id_token.verify_oauth2_token(
                attrs['token'], requests.Request(), client_id
            )

            # Only accept verified email addresses
            if not google_id.get('email_verified', False):
                raise ValidationError({'token': ['Email not verified']})
            return google_id
        except (ValueError, GoogleAuthError) as err:
            raise ValidationError({'token': [str(err)]})


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()
    reset_form = None

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = PasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'request': request,
            'use_https': request.is_secure(),
            'token_generator': default_token_generator,
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'email_template_name': 'mails/password_reset.txt',
            'extra_email_context': {
                'reset_url': getattr(settings, 'PASSWORD_RESET_URL')
            },
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset attempt.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    _errors = {}
    user = None
    set_password_form = None

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        # Decode the uidb64 to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = accounts.User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, accounts.User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = SetPasswordForm(user=self.user, data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        return self.set_password_form.save()

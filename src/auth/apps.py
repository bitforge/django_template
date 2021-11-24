from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    default = True
    name = 'auth'
    verbose_name = _('Auth')


from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    default = True
    name = 'account'
    verbose_name = _('Accounts & Permissions')

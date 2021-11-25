import sys

from django.apps import AppConfig, apps
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    default = True
    name = 'account'
    verbose_name = _('Accounts & Permissions')

    def ready(self):
        # Show Groups in account app
        if all(cmd not in sys.argv for cmd in ['migrate', 'migration']):
            apps.get_model('auth.Group')._meta.app_label = 'account'
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiConfig(AppConfig):
    default = True
    name = 'api'
    verbose_name = _('API')

from django.apps import AppConfig
from django.conf import settings
from django.core import checks
from django.utils.translation import gettext_lazy as _


class MainAppConfig(AppConfig):
    default = True
    name = '{{ project_name }}'
    verbose_name = _('{{ project_name }}')


@checks.register
def check_db_env(app_configs, **kwargs):
    warnings = []
    db_name = settings.DATABASES['default']['ENGINE']
    db_host = settings.DATABASES['default']['HOST']
    is_sqlite = 'sqlite3' in db_name
    is_local = 'localhost' in db_host or '/var/run/postgresql' in db_host
    if settings.DEBUG and not is_sqlite and not is_local:
        warnings.append(
            checks.Warning(
                'DB is not local, you are probably using a Google Cloud env!',
                hint='Switch to local env with command: ln -sf envs/local.env .env',
                id='{{ project_name }}.W001',
            )
        )
    return warnings

from django.apps import AppConfig
from django.conf import settings
from django.core import checks


class MainAppConfig(AppConfig):
    default = True
    name = 'app'


@checks.register
def check_db_env(app_configs, **kwargs):
    warnings = []
    db_name = settings.DATABASES['default']['ENGINE']
    db_host = settings.DATABASES['default']['HOST']
    is_sqlite = 'sqlite3' in db_name
    is_local = 'localhost' in db_host
    if settings.DEBUG and not is_sqlite and not is_local:
        warnings.append(
            checks.Warning(
                "DB is not local, you are probably using a Google Cloud env!",
                hint="Switch to local env with command: ln -sf envs/local.env .env",
                id="app.W001",
            )
        )
    return warnings

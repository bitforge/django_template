from django.apps import AppConfig
from django.conf import settings
from django.core import checks
from django.utils.translation import gettext_lazy as _

from imagefield.fields import ImageField, ImageFieldFile


class MainAppConfig(AppConfig):
    default = True
    name = '{{ project_name }}'
    verbose_name = _('{{ project_name }}')

    def ready(self):
        monkey_patch_imagefield()


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
                "DB is not local, you are probably using a Google Cloud env!",
                hint="Switch to local env with command: ln -sf envs/local.env .env",
                id="{{ project_name }}.W001",
            )
        )
    return warnings


# ImageField customizations
def monkey_patch_imagefield():
    def check_size_only(self, **kwargs):
        """
        Suppress ImageField without ppoi warnings - check size only
        """
        errors = super(ImageField, self).check(**kwargs)
        if not self.width_field or not self.height_field:
            errors.append(
                checks.Error(
                    "ImageField without width_field/height_field is slow!",
                    hint="auto_add_fields=True automatically adds the fields.",
                    obj=self,
                    id="imagefield.E001",
                )
            )
        return errors

    def do_not_clear_anything(self, fieldfile, filename):
        pass

    ImageField.check = check_size_only
    ImageFieldFile._clear_generated_files_for = do_not_clear_anything

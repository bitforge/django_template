from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from reversion.admin import VersionAdmin

from {{ project_name }} import models
from {{ project_name }}.admin_utils import thumbnail_field

# Django Admin docs:
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/contrib/admin/


@admin.register(models.Entry)
class EntryAdmin(VersionAdmin):
    search_fields = ('title', 'description')
    list_display = (thumbnail_field('image', 'title'), 'modified')
    prepopulated_fields = {"slug": ("title",)}
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from reversion.admin import VersionAdmin

from {{ project_name }} import models
from admin.utils import thumbnail_title

# Django Admin docs:
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/contrib/admin/


class EntryAdmin(VersionAdmin):
    search_fields = ('title', 'description')
    list_display = (thumbnail_title('image', 'title'), 'modified')
    prepopulated_fields = {'slug': ('title',)}

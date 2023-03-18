from django.db import models

from reversion.admin import VersionAdmin

from admin.utils import thumbnail_title
from admin.widgets import AutosizeTextArea, MarkdownTextArea, AdminImageWidget

# Django Admin docs:
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/contrib/admin/


class EntryAdmin(VersionAdmin):
    search_fields = ('title', 'description')
    list_display = (thumbnail_title('image', 'title'), 'modified')
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
        models.TextField: {'widget': AutosizeTextArea},
    }


class TemplateAdmin(VersionAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    formfield_overrides = {
        models.TextField: {'widget': MarkdownTextArea},
    }

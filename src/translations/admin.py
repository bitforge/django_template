from django.contrib import admin
from django.db.models import TextField

from reversion.admin import VersionAdmin

from admin_ordering.admin import OrderableAdmin

from admin import widgets
from translations import models


class MessageInlineAdmin(OrderableAdmin, admin.TabularInline):
    ordering_field = 'order'
    ordering_field_hide_input = True
    fields = ['key', 'de', 'en', 'order']
    model = models.Message
    extra = 0
    formfield_overrides = {
        TextField: {'widget': widgets.AutosizeTextArea},
    }

@admin.register(models.Group)
class GroupAdmin(OrderableAdmin, VersionAdmin):
    ordering_field = 'order'
    ordering_field_hide_input = True
    list_display = ['name', 'key', 'order']
    list_editable = ['order']
    search_fields = ['name']
    exclude = ['order']
    inlines = [MessageInlineAdmin]


@admin.register(models.Message)
class MessageAdmin(VersionAdmin):
    ordering = ('group__order', 'order')
    list_display = ['full_key', 'de', 'en']
    list_display_links = None
    list_editable = ['de', 'en']
    list_filter = ['group']
    search_fields = ['key', 'de', 'en']
    exclude = ['group', 'order']
    formfield_overrides = {
        TextField: {'widget': widgets.AutosizeTextArea},
    }

    def full_key(self, obj):
        return "%s.%s" % (obj.group.key, obj.key)
    full_key.short_description = 'Key'

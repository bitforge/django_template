from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from account import models


@admin.register(models.User)
class UserAdmin(AuthUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    filter_horizontal = ['groups']
    readonly_fields = ['last_login', 'date_joined']
    ordering = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def get_fieldsets(self, request, obj):
        """
        Only allow admins to view and edit permissions
        """
        fields = super().get_fieldsets(request, obj=obj)
        if not request.user.is_superuser:
            fields = tuple(filter(lambda x: x[0] != _('Permissions'), fields))
        return fields

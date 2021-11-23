from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission


class YagoModelBackend(ModelBackend):
    """
    Limits readonly admins to view permissions
    """

    def _get_permissions(self, user_obj, obj, from_name):
        # Add all view permissions for readonly admins
        perm_cache_name = '_%s_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_readonly_superuser:
                perms = Permission.objects.filter(codename__startswith='view')
                perms = perms.values_list('content_type__app_label', 'codename').order_by()
                setattr(user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms})

        return super()._get_permissions(user_obj, obj, from_name)

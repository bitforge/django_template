from django.contrib.admin.apps import AdminConfig
from django.utils.translation import gettext_lazy as _


class AdminApp(AdminConfig):
    default_site = 'admin.site.AdminSite'

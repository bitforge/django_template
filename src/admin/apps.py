from django.contrib.admin.apps import AdminConfig


class AdminApp(AdminConfig):
    default_site = 'admin.site.AdminSite'

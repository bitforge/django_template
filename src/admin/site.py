from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import never_cache


class AdminSite(admin.AdminSite):
    def __init__(self, name='admin'):
        self.site_url = None
        self.final_catch_all_view = False
        super().__init__(name=name)

    @never_cache
    def login(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context['google_client_id'] = settings.GOOGLE_OAUTH_CLIENT_ID
        return super().login(request, extra_context)

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Move auth models to account
        if 'auth' in app_dict and 'account' in app_dict:
            auth_models = app_dict['auth']['models']
            app_dict['account']['models'].extend(auth_models)
            del app_dict['auth']

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list

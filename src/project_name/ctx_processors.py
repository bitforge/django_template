from django.conf import settings


def google_client_id(request):
    """
    Inject Google OAuth Client ID to context
    """
    return {'GOOGLE_OAUTH_CLIENT_ID': settings.GOOGLE_OAUTH_CLIENT_ID}
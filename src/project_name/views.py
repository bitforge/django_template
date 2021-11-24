from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.urls import reverse


def index(request):
    """
    Root redirect. Replace this with a redirect to frontend.
    """
    admin_url = reverse('admin:index')
    return HttpResponseRedirect(admin_url)


def favicon(request):
    """
    Quick favicon redirect.
    """
    favicon_url = static('img/favicons/favicon-32.png')
    return HttpResponseRedirect(favicon_url)

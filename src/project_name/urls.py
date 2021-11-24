
"""
{{ project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/{{ docs_version }}/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from {{ project_name }} import views

media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Genie Backend urls
urlpatterns = [
    path('', views.index, name='index_redirect'),
    path('favicon.ico', views.favicon, name='favicon_redirect'),
]

# Included urls
urlpatterns += [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
] + media_urls

# Only enable debug toolbar when installed
try:
    import debug_toolbar  # noqa
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
except ImportError:
    pass

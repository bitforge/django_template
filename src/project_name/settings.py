'''
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django {{ django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
'''

import os
import sys
import environ
from datetime import timedelta
from urllib.parse import urlparse
from django.core.exceptions import ImproperlyConfigured
from corsheaders.defaults import default_methods as cors_default_methods
from corsheaders.defaults import default_headers as cors_default_headers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SRC_DIR)

# ENV vars schema
# For development, these values will be read from .env file
# .env is usually a Symlink to the currently active environment (DEV, TEST, PROD)
# In production, all variables are expected as 12factor env vars
# It's good practice to mention all configurable values here!
env = environ.Env(
    # General settings
    HOST_URL=(str, 'http://localhost:8000'),
    SECRET_KEY=(str, None),
    DEBUG=(bool, False),
    MAINTENANCE_MODE=(bool, False),
    DATABASE_URL=(str, None),
    CACHE_URL=(str, 'locmemcache://'),
    GS_BUCKET_NAME=(str, None),
    GS_PROJECT_ID=(str, None),
    STORE_CDN_HOST=(str, None),
    EMAIL_HOST_USER=(str, 'no-reply@bitforge.ch'),
    EMAIL_HOST_PASSWORD=(str, None),
    PASSWORD_RESET_URL=(str, None),
    SENTRY_DSN=(str, None),
    GOOGLE_OAUTH_CLIENT_ID=(str, ''),
    GOOGLE_OAUTH_CLIENT_SECRET=(str, ''),
)

# Import settings from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='{{ secret_key }}')

# DEBUG is only enalbed when explicity configured in environment!
DEBUG = env('DEBUG')
if 'test' in sys.argv:
    DEBUG = True

# A list of IP addresses, that:
# * Allow the debug() context processor to add some variables to the template context.
# * Can use the admindocs bookmarklets even if not logged in as a staff user.
# * Changes the way how logging messages are sent to Admins (With Full Stack Traces).
INTERNAL_IPS = ['[::1]', '127.0.0.1']

# HOST_URL must be a valid URL and either start with 'http://' or 'https://'
# Valid URL structure: scheme://hostname<:port>/
# https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse
try:
    HOST_URL: str = env('HOST_URL')
    url = urlparse(HOST_URL)
    if url.scheme not in ['http', 'https']:
        raise ImproperlyConfigured('HOST_URL must start with "http://" or "https://".')
    if url.path not in ['', '/'] or url.query or url.fragment:
        raise ImproperlyConfigured('Please set HOST_URL to something simple like "https//domain.tld/"')
except ValueError:
    raise ImproperlyConfigured('HOST_URL must be a valid URL. Something like "https//domain.tld/"')

# HOST_NAME is derived from HOST_URL to prevent Host Header attacks.
try:
    HOST_NAME = urlparse(HOST_URL).hostname
except ValueError as error:
    raise ImproperlyConfigured(f'Could not derive HOST_NAME from HOST_URL!\n{error}')

# List of host/domain names to serve.
# This is a security measure to prevent HTTP Host header attacks.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std:setting-ALLOWED_HOSTS
ALLOWED_HOSTS = [HOST_NAME, ]

# Required to work nicely behind proxies
# https://docs.djangoproject.com/en/4.1/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = [HOST_URL, ]

# Enable secure cookies for CSRF and sessions in production by default.
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/security/#ssl-https
USE_SECURE_COOKIES = HOST_URL.startswith('https://')
CSRF_COOKIE_SECURE = USE_SECURE_COOKIES
SESSION_COOKIE_SECURE = USE_SECURE_COOKIES

# Set HTTP Strict Transport Policy Header when using https://
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Support https:// protocol when building absolute urls behind a proxy.
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow iframe embedding for related model admin (django-admin-interface feature)
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Required for Google Sign-In for Websites via Javascript
# Deprecation Memo: https://developers.googleblog.com/2021/08/gsi-jsweb-deprecation.html
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# CORS Headers
# https://github.com/adamchainz/django-cors-headers
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = list(cors_default_methods)
CORS_ALLOW_HEADERS = list(cors_default_headers) + ['content-disposition']

# Application definition
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin.apps.AdminApp',
    'api',
    'account',
    'translations',
    '{{ project_name }}',
    # Libraries
    'reversion',
    'corsheaders',
    'admin_ordering',
    'maintenance_mode',
    'versatileimagefield',
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

try:
    import debug_toolbar  # noqa
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')
except ImportError:
    pass

# Starting point for all mapped urls.
ROOT_URLCONF = '{{ project_name }}.urls'

# Disables all urls during maintenance work.
# Returns HTTP 503: Service unavailable on all requests when activated.
# https://github.com/fabiocaccamo/django-maintenance-mode
MAINTENANCE_MODE = env('MAINTENANCE_MODE')

# Template engine config
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/templates/#configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'src', '{{ project_name }}', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

# Cache Config
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/cache/
CACHES = {
    'default': env.cache()
}

# Use cached sessions with writethrough to db
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

# Using sqlite fallback for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Use postgres db when configured in env
# Google Cloud SQL is injected via UNIX Socket path:
# psql://<USER>:<PW>@//<SOCKET_PATH>/<DB_NAME>
if env('DATABASE_URL') and 'test' not in sys.argv:
    DATABASES = {'default': env.db_url('DATABASE_URL')}

# Mail settings
# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-EMAIL_HOST
if env('EMAIL_HOST_USER') and env('EMAIL_HOST_PASSWORD'):
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_TIMEOUT = 30
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
elif DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
PASSWORD_RESET_URL = env('PASSWORD_RESET_URL')

# Login url when password reset by mail is completed
LOGIN_URL = '/admin/login/'

# Google Single Sign On Javascript API credentials
GOOGLE_OAUTH_CLIENT_ID = env('GOOGLE_OAUTH_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET = env('GOOGLE_OAUTH_CLIENT_SECRET')

# User media files (uploaded images, 3D models and more)
# https://docs.djangoproject.com/en/3.1/topics/files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Use Goolge Cloud Storage when configured
if env('GS_BUCKET_NAME'):
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = env('GS_BUCKET_NAME')
    GS_PROJECT_ID = env('GS_PROJECT_ID')

    # Uniform storage buckets, disable signed urls
    GS_DEFAULT_ACL = None
    GS_QUERYSTRING_AUTH = False

    # Serve assets over keycdn
    GS_CUSTOM_ENDPOINT = env('STORE_CDN_HOST')

    # Allow caching assets up to 24h
    GS_CACHE_CONTROL = 'public, max-age=86400'

    # If a uploaded file already exists, append some extra charactes
    GS_FILE_OVERWRITE = False


# Static media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

if 'test' not in sys.argv:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Disable whitenoise startup delay
WHITENOISE_AUTOREFRESH = True

# Password validation
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
    ('fr', 'French'),
    ('it', 'Italian')
]

TRANSLATION_LANGUAGES = ['en', 'de']

LANGUAGE_COOKIE_NAME = 'language'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'src/{{ project_name }}/locale'),)

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default time zone (UTC +01:00, UTC DST +02:00)
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/timezones/
TIME_ZONE = 'Europe/Zurich'

# Custom user model
AUTH_USER_MODEL = 'account.user'

# Django REST Framework Api
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissions'],
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'api.negotiation.JsonAllTheThings',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'api.exceptions.exception_handler',
}

# OpenAPI 3.0 schema generation
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    'TITLE': '{{ project_name }} API',
    'DESCRIPTION': 'Have a nice day!',
    'VERSION': '1.0.0',
    'TOS': 'https://bitforge.ch/agb/',
    'CONTACT': {'name': 'Team at Bitforge AG', 'email': 'info@bitforge.ch'},
    'SERVERS': [{'url': HOST_URL}],
    'SERVE_INCLUDE_SCHEMA': False,
}

# Simple JWT Token for API
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'sub',
    'AUDIENCE': HOST_URL,
    'ISSUER': HOST_URL,
}

# Preprocessed images
# Image renditions - default sizes for image
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'thumbnails': [
        ('url', 'url'),
        ('thumb', 'thumbnail__120x120'),
        ('preview', 'thumbnail__360x360'),
    ],
}

# sentry.io error reporting
if env('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True,
    )

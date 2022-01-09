"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django {{ django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

import os
import sys
import environ
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SRC_DIR)

# ENV vars schema
# For development, these values will be read from .env file
# In production, all variables are expected as 12factor env vars
# TL/DR: It's good practice to mention all configurable values here
env = environ.Env(
    # General settings
    SECRET_KEY=(str, None),
    DEBUG=(bool, False),
    MAINTENANCE_MODE=(bool, False),
    DATABASE_URL=(str, None),
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

# DEBUG set to true if env variable is set
DEBUG = env('DEBUG')
if 'test' in sys.argv:
    DEBUG = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

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
    'account',
    'api',
    '{{ project_name }}',
    # Libraries
    'maintenance_mode',
    'imagefield',
    'reversion',
    'rest_framework',
    'drf_spectacular',
    'corsheaders',
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
    import debug_toolbar # noqa
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')
except ImportError:
    pass


# Set HTTP Strict Transport Policy to access only using https://
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Support https:// proctocol when behind a proxy and building absolute urls
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow iframe embedding for related model admin
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Starting point for all mapped urls
ROOT_URLCONF = '{{ project_name }}.urls'

# Max request body size for file uploads over api: 30MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024

# Use cache for session with writethrough to db
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

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
            ],
        },
    },
]

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

# Maintenance mode
# Disables the whole backend during maintenance work.
# Returns HTTP 503: Service unavailable on all requests when activated.
# https://github.com/fabiocaccamo/django-maintenance-mode
MAINTENANCE_MODE = env('MAINTENANCE_MODE')


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

# Using sqlite fallback for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Use postgres db when configured in env
# Google Cloud SQL is injected via UNIX Socket path:
# psql://<USER>:<PW>@//<SOCKET_PATH>/<DB_NAME>
if env('DATABASE_URL') and 'test' not in sys.argv:
    DATABASES = {'default': env.db_url('DATABASE_URL')}

# Avoid unnecessary migrations to BigAutoFields
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

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
    GS_CACHE_CONTROL = "public, max-age=86400"

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
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

# FR and IT are required for language switching, but are not translated

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
    ('fr', 'French'),
    ('it', 'Italian'),
]

LANGUAGE_COOKIE_NAME = 'language'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'src/{{ project_name }}/locale'),
)

TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Custom user model
AUTH_USER_MODEL = 'account.user'

# Django REST Framework Api
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'api.negotiation.JsonAllTheThings',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'api.exceptions.exception_handler',
}


SPECTACULAR_SETTINGS = {
    'TITLE': '{{ project_name }} API',
    'DESCRIPTION': 'Have a nice day!',
    'VERSION': '1.0.0',
    'TOS': 'https://bitforge.ch/agb/',
    'CONTACT': {
        'name': 'Team at Bitforge AG',
        'email': 'info@bitforge.ch',
    },
    'SERVE_INCLUDE_SCHEMA': False,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
}

# Preprocessed images
IMAGEFIELD_FORMATS = {
    '{{ project_name }}.entry.image': {
        'thumb': ['default', ('thumbnail', (120, 120))],
        'preview': ['default', ('thumbnail', (300, 300))],
    },
}

# CORS Headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'accept-language',
    'authorization',
    'content-type',
    'content-disposition',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# sentry.io error reporting
if env('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True
    )
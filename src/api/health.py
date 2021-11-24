
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.cache import cache

from account import models as accounts


def check_db():
    try:
        return accounts.User.objects.exists()
    except accounts.User.DoesNotExist:
        return False


def check_storage():
    try:
        storage, filename = default_storage, 'health.txt'
        storage.save(filename, ContentFile(content=b'healt_check'))
        storage_up = storage.exists(filename)
        storage.delete(filename)
        return storage_up
    except Exception:
        return False


def check_cache():
    try:
        cache.set('health', 'check', 10)
        cache_up = cache.get('health') == 'check'
        cache.delete('health')
        return cache_up
    except Exception:
        return False

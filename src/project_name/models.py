import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from imagefield.fields import ImageField

# Django models doc:
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/db/models/


def entry_upload_path(instance, filename):
    return os.path.join('images', 'entry', instance.slug, filename)


# Rename this class
class Entry(models.Model):
    """
    Template model - adapt to your project
    """

    # Always use uuid as primary key!
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(_('Title'), max_length=100)

    slug = models.SlugField(_('Slug'), max_length=100)

    image = ImageField(_('Image'), upload_to=entry_upload_path, blank=True, null=True,
        auto_add_fields=True, ppoi_field=False,)

    website = models.URLField(_('Website'), blank=True, null=True)

    description = models.TextField(_('Description'), blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
        ordering = ('title',)

    def __str__(self):
        return self.title

    @property
    def image_thumb(self):
        return self.image.thumb if self.image else None

    @property
    def image_preview(self):
        return self.image.preview if self.image else None
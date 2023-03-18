import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

# Django models doc:
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/db/models/


class Entry(models.Model):
    """
    Template model - adapt it to your project and write a description here
    """

    # Always use uuid as primary key!
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(_('Title'), max_length=100)

    slug = models.SlugField(_('Slug'), max_length=100)

    image = VersatileImageField(_('Image'), upload_to='entries/', blank=True, null=True)

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


# Signals
# https://docs.djangoproject.com/en/4.0/topics/signals/


def preprocess_images(sender, instance, **kwargs):
    """
    Preprocesses thumbnails when mobyz object is saved
    """
    if instance.image:
        VersatileImageFieldWarmer(
            instance_or_queryset=instance,
            rendition_key_set='thumbnails',
            image_attr='image',
        ).warm()


post_save.connect(preprocess_images, sender=Entry)

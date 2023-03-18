from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField(max_length=200)

    key = models.CharField('Key', max_length=200)

    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __str__(self):
        return self.name


class Text(models.Model):
    key = models.CharField('Key', max_length=200)

    group = models.ForeignKey(
        to=Group,
        verbose_name=_('Group'),
        related_name='texts',
        on_delete=models.CASCADE,
    )

    order = models.PositiveIntegerField(_('Order'), default=0)

    de = models.TextField(_('German'))
    en = models.TextField(_('English'), blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('Text')
        verbose_name_plural = _('Texts')

    def __str__(self):
        return self.key

    @property
    def full_key(self, text):
        return "%s.%s" % (text.group.key, text.key)

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from account import managers


class User(AbstractUser):
    """
    Custom user model for extendability, identified by email address
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.EmailUserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} <{self.email}>'
        else:
            return self.email

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        # Fallback to username from email
        return self.email.split("@")[0]

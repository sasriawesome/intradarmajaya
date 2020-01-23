import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ Custom User Model """

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, verbose_name=_('UUID'))

    @property
    def is_person(self):
        person = getattr(self, 'person', None)
        return bool(person)

    @property
    def fullname(self):
        person = getattr(self, 'person', None)
        name = self.get_full_name()
        if person:
            name = person.fullname
        return name

    @property
    def is_admin(self):
        return self.is_superuser

    def __str__(self):
        fname = self.username if self.fullname in [None, ''] else self.fullname
        return fname
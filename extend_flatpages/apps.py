__author__ = 'igor'

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FlatPagesConfig(AppConfig):
    name = 'extend_flatpages'
    verbose_name = _("Flat Pages")
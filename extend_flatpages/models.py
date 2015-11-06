# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ExtendedFlatPage(FlatPage):
    meta_keywords = models.TextField(verbose_name=u'Мета тег: keywords', blank=True)
    meta_description = models.TextField(verbose_name=u'Мета тег: description', blank=True)
    meta_title = models.CharField(verbose_name=u'Мета тег: title', blank=True, max_length=500)

    class Meta:
        verbose_name = u'Расширенная простая страница'
        verbose_name_plural = u'Расширенные простые страницы'

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)
__author__ = 'igor'

from django.contrib import sitemaps
from extend_flatpages.models import ExtendedFlatPage


class ExtendFlatPage(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ExtendedFlatPage.objects.all()
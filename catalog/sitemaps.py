from django.contrib.sitemaps import Sitemap
from catalog.models import Category, Product


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Category.objects.filter(enable=True)

    def lastmod(self, obj):
        return obj.date_last_modified


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Product.objects.filter(enable=True)

    def lastmod(self, obj):
        return obj.date_last_modified
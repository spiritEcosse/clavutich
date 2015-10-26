from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    title = models.CharField(verbose_name=_('Title category'), max_length=200)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), related_name='categories', blank=True, null=True,
                            db_index=True)
    image = models.ImageField(verbose_name=_('Main image'), upload_to='images/catalog/category/%Y/%m/')
    slug = models.SlugField(verbose_name=_('Slug'), max_length=200, unique=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    enable = models.BooleanField(verbose_name=_('Enable'), default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    sort = models.IntegerField(verbose_name=_('Sort'), blank=True, default=0)

    _slug_separator = '/'

    class MPTTMeta:
        ordering = ['tree_id', 'lft']

    class Meta:
        ordering = ('sort', 'title', '-date_last_modified')
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    def get_ancestors_and_self(self):
        """
        Gets ancestors and includes itself. Use treebeard's get_ancestors
        if you don't want to include the category itself. It's a separate
        function as it's commonly used in templates.
        """
        return list(self.get_ancestors()) + [self]

    def full_slug(self):
        slugs = [category.slug for category in self.get_ancestors_and_self()]
        return self._slug_separator.join(slugs)

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.full_slug()})

    def image_preview(self):
        return u'<img style="max-width:100px; max-height:100px" src="%s" />' % self.image.url
    image_preview.short_description = _('Image')
    image_preview.allow_tags = True


class Product(models.Model):
    title = models.CharField(verbose_name=_('Title product'), max_length=200)
    image = models.ImageField(verbose_name=_('Main image'), upload_to='images/catalog/product/%Y/%m/')
    slug = models.SlugField(verbose_name=_('Slug'), max_length=200, unique=True)
    category = models.ForeignKey('Category', verbose_name=_('Categories'), related_name='products')
    description = models.TextField(verbose_name=_('Description'))
    enable = models.BooleanField(verbose_name=_('Enable'), default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    sort = models.IntegerField(verbose_name=_('Sort'), blank=True, default=0)

    _slug_separator = '/'

    class Meta:
        ordering = ('sort', 'title', '-date_last_modified')
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug, 'category_slug': self.category.full_slug()})

    def image_preview(self):
        return u'<img style="max-width:100px; max-height:100px" src="%s" />' % self.image.url
    image_preview.short_description = _('Image')
    image_preview.allow_tags = True



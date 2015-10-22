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

    class MPTTMeta:
        ordering = ['tree_id', 'lft']

    class Meta:
        ordering = ('sort', 'title', '-date_last_modified')
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    def get_tree_group(self, branch):
        if self.parent:
            branch.append(self.parent.slug)
            self.parent.get_tree_group(branch)

        return branch

    def slug_to_string(self):
        slug = list()
        slug.append(self.slug)
        slug.extend(self.get_tree_group([]))
        return '/'.join(map(str, reversed(slug)))

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug_to_string()})

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

    class Meta:
        ordering = ('sort', 'title', '-date_last_modified')
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug, 'slug': self.category.slug})

    def image_preview(self):
        return u'<img style="max-width:100px; max-height:100px" src="%s" />' % self.image.url
    image_preview.short_description = _('Image')
    image_preview.allow_tags = True



# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from clavutich import settings
from django_select2.forms import Select2Widget
from django.db import models


class Category(MPTTModel):
    title = models.CharField(verbose_name=u'Название категории', max_length=200)
    parent = TreeForeignKey('self', verbose_name=u'Родительская категория', related_name='categories', blank=True, null=True,
                            db_index=True)
    image = models.ImageField(verbose_name=u'Главное изображение', blank=True, upload_to='images/catalog/category/%Y/%m/',
                              default=settings.IMAGE_NOT_FOUND)
    slug = models.SlugField(verbose_name=u'Ссылка', max_length=200, unique=True)
    description = RichTextUploadingField(verbose_name=u'Описание', blank=True)
    enable = models.BooleanField(verbose_name=u'Включено', default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    sort = models.IntegerField(verbose_name=u'Сортировка', blank=True, default=0)
    meta_keywords = models.TextField(verbose_name=u'Мета тег: keywords', blank=True)
    meta_description = models.TextField(verbose_name=u'Мета тег: description', blank=True)
    meta_title = models.CharField(verbose_name=u'Мета тег: title', blank=True, max_length=500)

    _slug_separator = '/'

    class MPTTMeta:
        ordering = ['tree_id', 'lft']

    class Meta:
        ordering = ('sort', 'title', '-date_last_modified')
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

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
        if self.image:
            return u'<img style="max-width:100px; max-height:100px" src="%s" />' % self.image.url
    image_preview.short_description = u'Изображение'
    image_preview.allow_tags = True


class Product(models.Model):
    title = models.CharField(verbose_name=u'Название продукта', max_length=200)
    image = models.ImageField(verbose_name=u'Главное изображение', upload_to='images/catalog/product/%Y/%m/', null=True,
                              blank=True, default=settings.IMAGE_NOT_FOUND)
    slug = models.SlugField(verbose_name=u'Ссылка', max_length=200, unique=True)
    category = models.ForeignKey('Category', verbose_name=u'Категория', related_name='products')
    description = RichTextUploadingField(verbose_name=u'Описание')
    enable = models.BooleanField(verbose_name=u'Включено', default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    sort = models.IntegerField(verbose_name=u'Сортировка', blank=True, default=0)
    meta_keywords = models.TextField(verbose_name=u'Мета тег: keywords', blank=True)
    meta_description = models.TextField(verbose_name=u'Мета тег: description', blank=True)
    meta_title = models.CharField(verbose_name=u'Мета тег: title', blank=True, max_length=500)

    _slug_separator = '/'

    class Meta:
        ordering = ('sort', 'title', '-date_last_modified')
        verbose_name = u'Продукт'
        verbose_name_plural = u'Продукты'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug, 'category_slug': self.category.full_slug()})

    def image_preview(self):
        if self.image:
            return u'<img style="max-width:100px; max-height:100px" src="%s" />' % self.image.url
    image_preview.short_description = u'Изображение'
    image_preview.allow_tags = True
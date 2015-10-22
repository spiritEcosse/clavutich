# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title category')),
                ('image', models.ImageField(upload_to=b'images/catalog/category/%Y/%m/', verbose_name='Main image')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('sort', models.IntegerField(default=0, verbose_name='Sort', blank=True)),
            ],
            options={
                'ordering': ('sort', 'title', '-date_last_modified'),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title product')),
                ('image', models.ImageField(upload_to=b'images/catalog/product/%Y/%m/', verbose_name='Main image')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_last_modified', models.DateTimeField(auto_now=True)),
                ('sort', models.IntegerField(default=0, verbose_name='Sort', blank=True)),
                ('categories', models.ManyToManyField(related_name='products', verbose_name='Categories', to='catalog.Category')),
            ],
            options={
                'ordering': ('sort', 'title', '-date_last_modified'),
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]

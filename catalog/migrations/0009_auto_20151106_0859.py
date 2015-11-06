# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20151104_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.TextField(verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: description', blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.TextField(verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: keywords', blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.CharField(max_length=500, verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: title', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.TextField(verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: description', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_keywords',
            field=models.TextField(verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: keywords', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title',
            field=models.CharField(max_length=500, verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: title', blank=True),
        ),
    ]

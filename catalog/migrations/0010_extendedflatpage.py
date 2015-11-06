# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
        ('catalog', '0009_auto_20151106_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedFlatPage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
                ('meta_keywords', models.TextField(verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: keywords', blank=True)),
                ('meta_description', models.TextField(verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: description', blank=True)),
                ('meta_title', models.CharField(max_length=500, verbose_name='\u041c\u0435\u0442\u0430 \u0442\u0435\u0433: title', blank=True)),
            ],
            bases=('flatpages.flatpage',),
        ),
    ]

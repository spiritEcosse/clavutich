# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20151020_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(related_name='categories', default=None, verbose_name='Parent', blank=True, null=True, to='catalog.Category'),
            preserve_default=False,
        ),
    ]

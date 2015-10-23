# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20151021_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(default=None, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(default=None, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(default=None, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(default=None, editable=False, db_index=True),
            preserve_default=False,
        ),
    ]

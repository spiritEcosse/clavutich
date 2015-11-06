# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_extendedflatpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendedflatpage',
            name='flatpage_ptr',
        ),
        migrations.DeleteModel(
            name='ExtendedFlatPage',
        ),
    ]

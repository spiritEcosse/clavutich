# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20151104_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=sorl.thumbnail.fields.ImageField(default=b'images/image_not_found.jpg', upload_to=b'images/catalog/category/%Y/%m/', verbose_name='\u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=sorl.thumbnail.fields.ImageField(default=b'images/image_not_found.jpg', upload_to=b'images/catalog/product/%Y/%m/', null=True, verbose_name='\u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435', blank=True),
        ),
    ]

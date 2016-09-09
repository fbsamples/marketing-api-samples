# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '9999_auto_samples_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='roles_to_check',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]

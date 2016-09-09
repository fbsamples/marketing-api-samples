# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbuserinrole',
            name='fb_userid',
            field=models.ForeignKey(to='common.FBUser'),
            preserve_default=True,
        ),
    ]

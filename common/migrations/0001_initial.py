# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FBUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('fb_userid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('fb_username', models.CharField(unique=True, max_length=50)),
                ('full_name', models.CharField(unique=False, max_length=61)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

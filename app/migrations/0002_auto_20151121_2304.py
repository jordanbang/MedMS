# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='location',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='day',
            field=models.CharField(db_index=True, max_length=3, choices=[(1, b'Monday'), (2, b'Tuesday'), (3, b'Wednesday'), (4, b'Thursday'), (5, b'Friday'), (6, b'Saturday'), (7, b'Sunday')]),
        ),
    ]

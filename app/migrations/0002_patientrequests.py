# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient', models.CharField(max_length=30, blank=True)),
                ('location', models.CharField(max_length=30, blank=True)),
                ('open', models.BooleanField(db_index=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-15 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0008_auto_20180312_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='jornada',
            field=models.CharField(default='1', max_length=25),
        ),
    ]

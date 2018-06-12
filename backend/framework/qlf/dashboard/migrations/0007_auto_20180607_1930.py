# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20180524_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposure',
            name='teldec',
            field=models.FloatField(blank=True, help_text='Central Dec of the exposure', null=True),
        ),
        migrations.AlterField(
            model_name='exposure',
            name='telra',
            field=models.FloatField(blank=True, help_text='Central RA of the exposure', null=True),
        ),
        migrations.AlterField(
            model_name='exposure',
            name='tile',
            field=models.IntegerField(blank=True, help_text='Tile ID', null=True),
        ),
    ]

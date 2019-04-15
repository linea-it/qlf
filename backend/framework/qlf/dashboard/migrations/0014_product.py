# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-29 16:08
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20181002_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('key', models.CharField(help_text='Metric Key', max_length=30)),
                ('mjd', models.FloatField(help_text='MJD', null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_job', to='dashboard.Job')),
            ],
        ),
    ]
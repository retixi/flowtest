# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-03 06:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlowTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('cate', models.CharField(max_length=30)),
                ('flow_data', models.FloatField()),
                ('last_date', models.DateField()),
                ('uni_count', models.IntegerField()),
                ('ne_name', models.CharField(max_length=100)),
                ('bu_peak', models.FloatField()),
                ('bu_busy_avg', models.FloatField()),
                ('bu_avg', models.FloatField()),
                ('port_name', models.CharField(max_length=100)),
                ('band_width', models.IntegerField()),
            ],
        ),
    ]
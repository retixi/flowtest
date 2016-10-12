# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-23 00:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_buildlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='linklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('intro', models.CharField(max_length=255)),
            ],
        ),
    ]

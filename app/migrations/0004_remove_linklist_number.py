# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-23 01:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_linklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linklist',
            name='number',
        ),
    ]
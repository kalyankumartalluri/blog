# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cqtest', '0003_remove_test_steps'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='tokenised',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='step expresult'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 00:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0016_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
    ]

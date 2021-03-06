# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0007_post_vote_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='vote_count',
            new_name='downvote_count',
        ),
        migrations.AddField(
            model_name='post',
            name='upvote_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

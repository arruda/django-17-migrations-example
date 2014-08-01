# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def voteFieldToModel(apps, schema_editor):
    "transform all vote field from choice Model to a vote model with root user as owner"

    Choice = apps.get_model("polls", "Choice")
    for choice in Choice.objects.all():
        for i in xrange(0, choice.votes):
            choice.vote_set.create()


def revert(apps, schema_editor):
    "revert back deleting the votes for a choice and adding it as a vote in the field"

    Choice = apps.get_model("polls", "Choice")
    for choice in Choice.objects.all():
        choice.vote = choice.vote_set.all().count()
        choice.vote_set.delete()
        choice.save()


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_vote'),
    ]

    operations = [
        migrations.RunPython(voteFieldToModel, reverse_code=revert),
    ]

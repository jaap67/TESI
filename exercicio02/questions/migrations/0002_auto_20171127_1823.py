# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-27 18:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question03',
            old_name='localizacao',
            new_name='localidade',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
            ],
            options={
                'verbose_name_plural': 'specifications',
                'verbose_name': 'specification',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SpecificationField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('type', models.CharField(choices=[(b'text', 'text'), (b'longtext', 'long text'), (b'boolean', 'boolean'), (b'integer', 'integer'), (b'closed_set_single', 'closed set'), (b'closed_set_multiple', 'closed set (multiple)'), (b'open_set_single', 'open set'), (b'open_set_single_extensible', b'open set (extensible)')], verbose_name='type', max_length=30)),
                ('choices', models.TextField(blank=True, verbose_name='choices', help_text='One choice per line (if applicable).')),
                ('help_text', models.CharField(blank=True, verbose_name='help text', max_length=100, default=b'')),
                ('required', models.BooleanField(verbose_name='required')),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
            ],
            options={
                'verbose_name_plural': 'specification fields',
                'verbose_name': 'specification field',
                'ordering': ['group__ordering', 'ordering'],
            },
        ),
        migrations.CreateModel(
            name='SpecificationFieldGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=100)),
                ('ordering', models.IntegerField(verbose_name='ordering', default=0)),
                ('specification', models.ForeignKey(to='specifications.Specification', related_name='groups', verbose_name='specification')),
            ],
            options={
                'verbose_name_plural': 'specification field groups',
                'verbose_name': 'specification field group',
                'ordering': ['ordering'],
            },
        ),
        migrations.AddField(
            model_name='specificationfield',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='specifications.SpecificationFieldGroup', blank=True, related_name='fields', verbose_name='group', null=True),
        ),
        migrations.AddField(
            model_name='specificationfield',
            name='specification',
            field=models.ForeignKey(to='specifications.Specification', related_name='fields', verbose_name='specification'),
        ),
    ]

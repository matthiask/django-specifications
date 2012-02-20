# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Specification'
        db.create_table('specifications_specification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('specifications', ['Specification'])

        # Adding model 'SpecificationFieldGroup'
        db.create_table('specifications_specificationfieldgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('specification', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups', to=orm['specifications.Specification'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('specifications', ['SpecificationFieldGroup'])

        # Adding model 'SpecificationField'
        db.create_table('specifications_specificationfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('choices', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('specification', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['specifications.Specification'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fields', null=True, to=orm['specifications.SpecificationFieldGroup'])),
        ))
        db.send_create_signal('specifications', ['SpecificationField'])

    def backwards(self, orm):
        # Deleting model 'Specification'
        db.delete_table('specifications_specification')

        # Deleting model 'SpecificationFieldGroup'
        db.delete_table('specifications_specificationfieldgroup')

        # Deleting model 'SpecificationField'
        db.delete_table('specifications_specificationfield')

    models = {
        'specifications.specification': {
            'Meta': {'ordering': "['name']", 'object_name': 'Specification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'specifications.specificationfield': {
            'Meta': {'ordering': "['group__ordering', 'ordering']", 'object_name': 'SpecificationField'},
            'choices': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fields'", 'null': 'True', 'to': "orm['specifications.SpecificationFieldGroup']"}),
            'help_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'specification': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': "orm['specifications.Specification']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'specifications.specificationfieldgroup': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'SpecificationFieldGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'specification': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'to': "orm['specifications.Specification']"})
        }
    }

    complete_apps = ['specifications']
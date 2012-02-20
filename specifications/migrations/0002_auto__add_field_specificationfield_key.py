# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SpecificationField.key'
        db.add_column('specifications_specificationfield', 'key',
                      self.gf('django.db.models.fields.CharField')(default='key', max_length=20),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'SpecificationField.key'
        db.delete_column('specifications_specificationfield', 'key')

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
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
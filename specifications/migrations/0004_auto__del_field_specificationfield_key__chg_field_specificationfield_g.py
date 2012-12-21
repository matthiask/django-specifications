# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SpecificationField.key'
        db.delete_column('specifications_specificationfield', 'key')


        # Changing field 'SpecificationField.group'
        db.alter_column('specifications_specificationfield', 'group_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['specifications.SpecificationFieldGroup']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'SpecificationField.key'
        raise RuntimeError("Cannot reverse this migration. 'SpecificationField.key' and its values cannot be restored.")

        # Changing field 'SpecificationField.group'
        db.alter_column('specifications_specificationfield', 'group_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['specifications.SpecificationFieldGroup']))

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
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fields'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['specifications.SpecificationFieldGroup']"}),
            'help_text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'specification': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': "orm['specifications.Specification']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Egg'
        db.create_table(u'gestus_egg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('package', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'gestus', ['Egg'])

        # Adding model 'EggVersion'
        db.create_table(u'gestus_eggversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('egg', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['gestus.Egg'])),
        ))
        db.send_create_signal(u'gestus', ['EggVersion'])

        # Adding model 'Website'
        db.create_table(u'gestus_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'gestus', ['Website'])

        # Adding model 'WebsiteEnvironment'
        db.create_table(u'gestus_websiteenvironment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(related_name='environments', to=orm['gestus.Website'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('server', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'gestus', ['WebsiteEnvironment'])

        # Adding M2M table for field eggs on 'WebsiteEnvironment'
        m2m_table_name = db.shorten_name(u'gestus_websiteenvironment_eggs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('websiteenvironment', models.ForeignKey(orm[u'gestus.websiteenvironment'], null=False)),
            ('eggversion', models.ForeignKey(orm[u'gestus.eggversion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['websiteenvironment_id', 'eggversion_id'])


    def backwards(self, orm):
        # Deleting model 'Egg'
        db.delete_table(u'gestus_egg')

        # Deleting model 'EggVersion'
        db.delete_table(u'gestus_eggversion')

        # Deleting model 'Website'
        db.delete_table(u'gestus_website')

        # Deleting model 'WebsiteEnvironment'
        db.delete_table(u'gestus_websiteenvironment')

        # Removing M2M table for field eggs on 'WebsiteEnvironment'
        db.delete_table(db.shorten_name(u'gestus_websiteenvironment_eggs'))


    models = {
        u'gestus.egg': {
            'Meta': {'object_name': 'Egg'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'package': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'gestus.eggversion': {
            'Meta': {'object_name': 'EggVersion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'egg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': u"orm['gestus.Egg']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'gestus.website': {
            'Meta': {'object_name': 'Website'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'gestus.websiteenvironment': {
            'Meta': {'object_name': 'WebsiteEnvironment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'eggs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gestus.EggVersion']", 'symmetrical': 'False', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'environments'", 'to': u"orm['gestus.Website']"})
        }
    }

    complete_apps = ['gestus']
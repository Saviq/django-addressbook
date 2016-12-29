# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CustomField'
        db.create_table('addressbook_customfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='custom_fields', to=orm['addressbook.Contact'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('addressbook', ['CustomField'])

        # Adding model 'Date'
        db.create_table('addressbook_date', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dates', to=orm['addressbook.Contact'])),
            ('value', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('addressbook', ['Date'])

        # Adding model 'EmailAddress'
        db.create_table('addressbook_emailaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_addresses', to=orm['addressbook.Contact'])),
            ('value', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('addressbook', ['EmailAddress'])

        # Adding model 'IMAccount'
        db.create_table('addressbook_imaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='im_accounts', to=orm['addressbook.Contact'])),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('account', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('addressbook', ['IMAccount'])

        # Adding model 'Link'
        db.create_table('addressbook_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['addressbook.Contact'])),
            ('value', self.gf('django.db.models.fields.URLField')(default='http://', max_length=200)),
        ))
        db.send_create_signal('addressbook', ['Link'])

        # Adding model 'Organization'
        db.create_table('addressbook_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizations', to=orm['addressbook.Contact'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('addressbook', ['Organization'])

        # Adding model 'PhoneNumber'
        db.create_table('addressbook_phonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='phone_numbers', to=orm['addressbook.Contact'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('addressbook', ['PhoneNumber'])

        # Adding model 'PostalAddress'
        db.create_table('addressbook_postaladdress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='postal_addresses', to=orm['addressbook.Contact'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('addressbook', ['PostalAddress'])

        # Adding model 'Contact'
        db.create_table('addressbook_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_company', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('addressbook', ['Contact'])

        # Adding model 'Group'
        db.create_table('addressbook_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('addressbook', ['Group'])

        # Adding M2M table for field members on 'Group'
        db.create_table('addressbook_group_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['addressbook.group'], null=False)),
            ('contact', models.ForeignKey(orm['addressbook.contact'], null=False))
        ))
        db.create_unique('addressbook_group_members', ['group_id', 'contact_id'])


    def backwards(self, orm):
        
        # Deleting model 'CustomField'
        db.delete_table('addressbook_customfield')

        # Deleting model 'Date'
        db.delete_table('addressbook_date')

        # Deleting model 'EmailAddress'
        db.delete_table('addressbook_emailaddress')

        # Deleting model 'IMAccount'
        db.delete_table('addressbook_imaccount')

        # Deleting model 'Link'
        db.delete_table('addressbook_link')

        # Deleting model 'Organization'
        db.delete_table('addressbook_organization')

        # Deleting model 'PhoneNumber'
        db.delete_table('addressbook_phonenumber')

        # Deleting model 'PostalAddress'
        db.delete_table('addressbook_postaladdress')

        # Deleting model 'Contact'
        db.delete_table('addressbook_contact')

        # Deleting model 'Group'
        db.delete_table('addressbook_group')

        # Removing M2M table for field members on 'Group'
        db.delete_table('addressbook_group_members')


    models = {
        'addressbook.contact': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Contact'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_company': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'addressbook.customfield': {
            'Meta': {'object_name': 'CustomField'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custom_fields'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'addressbook.date': {
            'Meta': {'object_name': 'Date'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dates'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.DateField', [], {})
        },
        'addressbook.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_addresses'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        'addressbook.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['addressbook.Contact']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'addressbook.imaccount': {
            'Meta': {'object_name': 'IMAccount'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'im_accounts'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'addressbook.link': {
            'Meta': {'object_name': 'Link'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.URLField', [], {'default': "'http://'", 'max_length': '200'})
        },
        'addressbook.organization': {
            'Meta': {'object_name': 'Organization'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizations'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'addressbook.phonenumber': {
            'Meta': {'object_name': 'PhoneNumber'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'phone_numbers'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'addressbook.postaladdress': {
            'Meta': {'object_name': 'PostalAddress'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'postal_addresses'", 'to': "orm['addressbook.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['addressbook']

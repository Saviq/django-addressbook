# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'PostalAddress.value'
        db.delete_column('addressbook_postaladdress', 'value')

        # Adding field 'PostalAddress.address1'
        db.add_column('addressbook_postaladdress', 'address1', self.gf('django.db.models.fields.CharField')(default='', max_length=127), keep_default=False)

        # Adding field 'PostalAddress.address2'
        db.add_column('addressbook_postaladdress', 'address2', self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True), keep_default=False)

        # Adding field 'PostalAddress.city'
        db.add_column('addressbook_postaladdress', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True), keep_default=False)

        # Adding field 'PostalAddress.state'
        db.add_column('addressbook_postaladdress', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=127, blank=True), keep_default=False)

        # Adding field 'PostalAddress.country'
        db.add_column('addressbook_postaladdress', 'country', self.gf('django.db.models.fields.CharField')(default='', max_length=127), keep_default=False)

        # Adding field 'PostalAddress.postcode'
        db.add_column('addressbook_postaladdress', 'postcode', self.gf('django.db.models.fields.CharField')(default='', max_length=31, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'PostalAddress.value'
        db.add_column('addressbook_postaladdress', 'value', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Deleting field 'PostalAddress.address1'
        db.delete_column('addressbook_postaladdress', 'address1')

        # Deleting field 'PostalAddress.address2'
        db.delete_column('addressbook_postaladdress', 'address2')

        # Deleting field 'PostalAddress.city'
        db.delete_column('addressbook_postaladdress', 'city')

        # Deleting field 'PostalAddress.state'
        db.delete_column('addressbook_postaladdress', 'state')

        # Deleting field 'PostalAddress.country'
        db.delete_column('addressbook_postaladdress', 'country')

        # Deleting field 'PostalAddress.postcode'
        db.delete_column('addressbook_postaladdress', 'postcode')


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
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'postal_addresses'", 'to': "orm['addressbook.Contact']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '31', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'})
        }
    }

    complete_apps = ['addressbook']

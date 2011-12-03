# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'WebToPayResponse.status'
        db.delete_column('webtopay_webtopayresponse', 'status')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'WebToPayResponse.status'
        raise RuntimeError("Cannot reverse this migration. 'WebToPayResponse.status' and its values cannot be restored.")


    models = {
        'webtopay.webtopayresponse': {
            'Meta': {'object_name': 'WebToPayResponse'},
            '_ss1': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            '_ss2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'orderid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'p_email': ('django.db.models.fields.TextField', [], {}),
            'payamount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'paycurrency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'payment': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'paytext': ('django.db.models.fields.TextField', [], {}),
            'projectid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'requestid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'surename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'test': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        }
    }

    complete_apps = ['webtopay']

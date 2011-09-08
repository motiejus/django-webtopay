# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WebToPayResponse'
        db.create_table('webtopay_webtopayresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ipaddress', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flag_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('projectid', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('orderid', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('payment', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('paytext', self.gf('django.db.models.fields.TextField')()),
            ('_ss2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('_ss1', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('surename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('test', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('p_email', self.gf('django.db.models.fields.TextField')()),
            ('requestid', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('payamount', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('paycurrency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('webtopay', ['WebToPayResponse'])


    def backwards(self, orm):
        
        # Deleting model 'WebToPayResponse'
        db.delete_table('webtopay_webtopayresponse')


    models = {
        'webtopay.webtopayresponse': {
            'Meta': {'object_name': 'WebToPayResponse'},
            '_ss1': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            '_ss2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'orderid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'p_email': ('django.db.models.fields.TextField', [], {}),
            'payamount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'paycurrency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'payment': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'paytext': ('django.db.models.fields.TextField', [], {}),
            'projectid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'requestid': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'surename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'test': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        }
    }

    complete_apps = ['webtopay']

# -*- coding: UTF-8 -*-

from urllib import unquote_plus, urlencode
import base64
import pdb

from django.test import TestCase
from django.test.client import Client

try:
    # Python 2.6 and later
    from urlparse import parse_qsl
except ImportError:
    # Python 2.5.  Works on Python 2.6 but raises PendingDeprecationWarning
    from cgi import parse_qsl

from webtopay.forms import WebToPayResponseForm, OrderedDict
from webtopay.signals import payment_was_successful, payment_was_flagged

# "answer" from libwebtopay test case
params = OrderedDict([
        ('wp_projectid', '13156'),
        ('wp_orderid', '1'),
        ('wp_lang', 'lit'),
        ('wp_amount', '10000'),
        ('wp_currency', 'LTL'),
        ('wp_payment', 'maximalt'),
        ('wp_country', 'LT'),
        ('wp_p_firstname', 'Vardenis'),
        ('wp_p_lastname', 'Pavardenis'),
        ('wp_p_email', 'm.sprunskas@evp.lt'),
        ('wp_p_street', 'Mėnulio g.7'),
        ('wp_p_city', 'Vilnius'),
        ('wp_test', '1'),
        ('wp_version', '1.4'),
        ('wp_type', 'EMA'),
        ('wp_paytext', 'Užsakymas nr: 1 http://test-project.local projekte. '\
                '(Pardavėjas: Libwebtopay Libwebtopay) (13156)'),
        ('wp_receiverid', '168328'),
        ('wp__ss1', 'c72cffd0345f55fef6595a86e5c7caa6'),
        ('wp_status', '1'),
        ('wp_requestid', '16309376'),
        ('wp_name', ''),
        ('wp_surename', ''),
        ('wp_payamount', '10000'),
        ('wp_paycurrency', 'LTL'),
        ('wp__ss2', 'oSiHSlnin/SSJ7bGaTWZybtHzA6/NaZcPtS3f07KZMoTeJteL6rnuw7q'\
                'fT/ACGW5Hifu2ieNnCBpu2XLnsR10Ja8/xVM5X7j2mg9wBOO1Y0cefKBSBlF'\
                'oZjLL2ciV32ETCD4Okxv2l/wH8tQhDQnJ6AOJkbh2ayKy8yTXOcE1zk=')])


class TestVerifications(TestCase):
    def testSS1(self):
        form = WebToPayResponseForm(params)
        self.assertTrue(form.check_ss1())

    def testSS2(self):
        form = WebToPayResponseForm(params)
        self.assertTrue(form.check_ss2())

    def testSS1Fail(self):
        params_c = params.copy()
        params_c['wp__ss1'] += 'bad'
        form = WebToPayResponseForm(params_c)
        self.assertFalse(form.check_ss1())

    def testSS2Fail(self):
        params_c = params.copy()
        params_c['wp__ss2'] = base64.encodestring('yammy')
        form = WebToPayResponseForm(params_c)
        self.assertFalse(form.check_ss2())

class TestSignals(TestCase):
    def setUp(self):
        self.client = Client()

    def testSuccess(self):
        self.got_signal = False

        def handle_signal(sender, **kargs):
            self.got_signal = True
            self.signal_obj = sender
        payment_was_successful.connect(handle_signal)
        resp = self.client.get('?' + urlencode(params))
        self.assertTrue(self.got_signal)

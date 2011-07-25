# -*- coding: UTF-8 -*-

from urllib import unquote_plus, urlencode
import base64
import pdb

from django.test import TestCase
from django.test.client import Client

from webtopay.forms import WebToPayResponseForm, OrderedDict
from webtopay.signals import payment_was_successful, payment_was_flagged

# query string from libwebtopay tests
query = 'wp_projectid=13156&wp_orderid=1&wp_lang=lit&wp_amount=10000&wp_curre'\
        'ncy=LTL&wp_payment=maximalt&wp_country=LT&wp_p_firstname=Vardenis&wp'\
        '_p_lastname=Pavardenis&wp_p_email=m.sprunskas%40evp.lt&wp_p_street=M'\
        '%C4%97nulio+g.7&wp_p_city=Vilnius&wp_test=1&wp_version=1.4&wp_type=E'\
        'MA&wp_paytext=U%C5%BEsakymas+nr%3A+1+http%3A%2F%2Ftest-project.local'\
        '+projekte.+%28Pardav%C4%97jas%3A+Libwebtopay+Libwebtopay%29+%2813156'\
        '%29&wp_receiverid=168328&wp__ss1=c72cffd0345f55fef6595a86e5c7caa6&wp'\
        '_status=1&wp_requestid=16309376&wp_name=&wp_surename=&wp_payamount=1'\
        '0000&wp_paycurrency=LTL&wp__ss2=oSiHSlnin%2FSSJ7bGaTWZybtHzA6%2FNaZc'\
        'PtS3f07KZMoTeJteL6rnuw7qfT%2FACGW5Hifu2ieNnCBpu2XLnsR10Ja8%2FxVM5X7j'\
        '2mg9wBOO1Y0cefKBSBlFoZjLL2ciV32ETCD4Okxv2l%2FwH8tQhDQnJ6AOJkbh2ayKy8'\
        'yTXOcE1zk%3D'

class TestVerifications(TestCase):
    def testSS1(self):
        form = WebToPayResponseForm(query)
        self.assertTrue(form.check_ss1())

    def testSS2(self):
        form = WebToPayResponseForm(query)
        self.assertTrue(form.check_ss2())

    def testSS1Fail(self):
        query2 = query.replace("c72cffd0345f55fef6595a86e5c7caa6", "bad")
        form = WebToPayResponseForm(query2)
        self.assertFalse(form.check_ss1())

    def testSS2Fail(self):
        query2 = query.replace('FxVM5X7j2mg9w', 'FxVM5X7j2mg9w'.swapcase())
        form = WebToPayResponseForm(query2)
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
        resp = self.client.get("?" + query)
        self.assertTrue(self.got_signal)

    def testBadSS1(self):
        self.got_signal = False
        def handle_signal(sender, **kargs):
            self.got_signal = True
            self.signal_obj = sender
        payment_was_flagged.connect(handle_signal)
        query2 = query.replace("c72cffd0345f55fef6595a86e5c7caa6", "bad")
        resp = self.client.get("?" + query2)
        self.assertTrue(self.got_signal)

    def testBadSS2(self):
        self.got_signal = False
        def handle_signal(sender, **kargs):
            self.got_signal = True
            self.signal_obj = sender
        payment_was_flagged.connect(handle_signal)
        query2 = query.replace('FxVM5X7j2mg9w', 'FxVM5X7j2mg9w'.swapcase())
        resp = self.client.get("?" + query2)
        self.assertTrue(self.got_signal)

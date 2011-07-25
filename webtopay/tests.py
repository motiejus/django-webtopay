from django.test import TestCase
from urlparse import urlparse
import pdb

try:
    # Python 2.6 and greater
    from urlparse import parse_qsl
except ImportError:
    # Python 2.5.  Works on Python 2.6 but raises PendingDeprecationWarning
    from cgi import parse_qsl

from forms import WebToPayResponseForm

# Urlencoded "answer" from libwebtopay test case
answer = 'http://www.webtopay.com/?testwp_answer=callback&wp_projectid=13156&wp_orderid=1&wp_lang=lit&wp_amount=10000&wp_currency=LTL&wp_payment=maximalt&wp_country=LT&wp_p_firstname=Vardenis&wp_p_lastname=Pavardenis&wp_p_email=m.sprunskas%40evp.lt&wp_p_street=M%C4%97nulio+g.7&wp_p_city=Vilnius&wp_test=1&wp_version=1.4&wp_type=EMA&wp_paytext=U%C5%BEsakymas+nr%3A+1+http%3A%2F%2Ftest-project.local+projekte.+%28Pardav%C4%97jas%3A+Libwebtopay+Libwebtopay%29+%2813156%29&wp_receiverid=168328&wp__ss1=c72cffd0345f55fef6595a86e5c7caa6&wp_status=1&wp_requestid=16309376&wp_name=&wp_surename=&wp_payamount=10000&wp_paycurrency=LTL&wp__ss2=oSiHSlnin%2FSSJ7bGaTWZybtHzA6%2FNaZcPtS3f07KZMoTeJteL6rnuw7qfT%2FACGW5Hifu2ieNnCBpu2XLnsR10Ja8%2FxVM5X7j2mg9wBOO1Y0cefKBSBlFoZjLL2ciV32ETCD4Okxv2l%2FwH8tQhDQnJ6AOJkbh2ayKy8yTXOcE1zk%3D'

query_tup = parse_qsl(urlparse(answer).query) # we are interested only in GET part
query = dict(query_tup[1:]) # removing ?testwp_answer=callback
SIGN_PASSWORD = '1c4196d0ff7fe4e94bdca98fb251bc25'

class TestRequest(TestCase):
    def testSs1(self):
        form = WebToPayResponseForm(query, password=SIGN_PASSWORD)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.check_ss1(SIGN_PASSWORD))

# -*- coding: UTF-8 -*-
import base64, re, logging, pdb
from M2Crypto import X509
from hashlib import md5
from urlparse import urlparse

try:
    from collections import OrderedDict # python 2.7 and above
except ImportError:
    from ordereddict import OrderedDict

try:
    from urlparse import parse_qsl # Python 2.6 and above
except ImportError:
    from cgi import parse_qsl

from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

from webtopay.cert import pem as cert_pem
from webtopay.widgets import ValueHiddenInput
from webtopay.models import WebToPayResponse
from webtopay.conf import WTP_PASSWORD, CHECK_SS1, CHECK_SS2,\
        BUTTON_HTML, POSTBACK_ENDPOINT

log = logging.getLogger(__name__)

class WebToPayResponseForm(forms.ModelForm):
    class Meta:
        model = WebToPayResponse

    def __init__(self, data_orig, **kargs):
        # Remove prefix from parameters
        data = OrderedDict(parse_qsl(urlparse(data_orig).path, keep_blank_values=True))
        data_trim = OrderedDict()
        for key, value in data.iteritems():
            data_trim[re.sub('^wp_', '', key)] = value

        super(WebToPayResponseForm, self).__init__(data_trim, **kargs)

    def badly_authorizes(self):
        if CHECK_SS1 and not self.check_ss1():
            return 'ss1'
        if CHECK_SS2 and not self.check_ss2():
            return 'ss2'
        return False

    def check_ss1(self):
        fields = [WTP_PASSWORD, self.data['orderid'], self.data['test'], '1']
        ss1 = Helpers.generate_ss1(fields, "|")
        if ss1 != self.data['_ss1']:
            return False
        return True

    def check_ss2(self):
        """ from libwebtopay:
        openssl_verify($_SS2, base64_decode($response['_ss2']), $pKeyP);
        foreach ($response as $key => $value) {
            if ($key!='_ss2') $_SS2 .= "{$value}|";
        }
        """
        fields = self.data.copy()
        sig = base64.decodestring(fields.pop('_ss2'))

        verify_msg = "|".join(fields.values()) + "|"

        pubkey = X509.load_cert_string(cert_pem).get_pubkey()
        pubkey.verify_init()
        pubkey.verify_update(verify_msg)
        if pubkey.verify_final(sig) != 1:
            return False
        return True


class WebToPaymentForm(forms.Form):
    projectid = forms.IntegerField(
            widget=ValueHiddenInput(),
            help_text="Unikalus projekto numeris. Tik patvirtinti projektai "\
                    "gali priimti įmokas")

    orderid = forms.CharField(max_length=40,
            widget=ValueHiddenInput(),
            help_text="Užsakymo numeris iš jūsų sistemos")

    lang = forms.CharField(max_length=3, required=False,
            widget=ValueHiddenInput(),
            help_text="Galima nurodyti naudotojo kalbą. Jeigu tokios kalbos "\
            "mokėjimai.lt nepalaiko bus parinkta kalba pagal lankytojo IP "\
            "adresą arba anglų kalba pagal nutylėjimą "\
            "(LIT, LAV, EST, RUS, ENG, GER, POL)")

    amount = forms.IntegerField(required=False,
            widget=ValueHiddenInput(),
            help_text="Suma centais, kurią klientas turi apmokėti")

    currency = forms.CharField(required=False, max_length=3,
            widget=ValueHiddenInput(),
            help_text="Mokėjimo valiuta (LTL, USD, EUR), kuria pageidaujate,"\
                    " kad klientas mokėtų. Jeigu nurodyta valiuta per "\
                    "pasirinktą mokėjimo būdą negali būti priimta, sistema "\
                    "automatiškai pagal dienos kursą konvertuos į palaikomą "\
                    "valiutą. Atsakyme į Jūsų svetainę bus paduoti payamount "\
                    "ir paycurrency")

    accepturl = forms.CharField(max_length=255,
            widget=ValueHiddenInput(),
            help_text="Pilnas interneto adresas (URL), į kurį klientas "\
                    "nukreipiamas sėkmingai atlikus mokėjimą")

    cancelurl = forms.CharField(max_length=255,
            widget=ValueHiddenInput(),
            help_text="Pilnas interneto adresas (URL), į kurį klientas "\
                    "nukreipiamas atšaukus ar nepavykus atlikti mokėjimą")

    callbackurl = forms.CharField(max_length=255,
            widget=ValueHiddenInput(),
            help_text="Pilnas adresas (URL), kuriuo pardavėjui pateikiama "\
                    "informacija apie atliktą mokėjimą")
    """
    Skriptas turi grąžinti tekstą "OK". Tik tuomet mūsų sistema užfiksuos, kad
    apie apmokėjimą sėkmingai informavome.  Jeigu atsakymo "OK" nėra, tai
    pranešimą siunčiame 4 kartus (kai tik gauname, po valandos, po trijų ir po
    paros).
    """

    payment = forms.CharField(max_length=20, required=False,
            widget=ValueHiddenInput(),
            help_text="Mokėjimo būdas. Parametras, kuriame nieko nenurodoma "\
                    "(paliekamas tuščias). Naudotojui bus pateikta lentelė "\
                    "su mokėjimo būdų sąrašu, pasirinkimui. Jis naudojamas "\
                    "tik tuo atveju, jeigu norima, kad mokėjimas būtų "\
                    "atliktas tik per konkretų mokėjimo būdą")

    country = forms.CharField(max_length=2, required=False,
            widget=ValueHiddenInput(),
            help_text="Mokėtojo šalis (LT, EE, LV, GB, PL, DE). Nurodžius "\
                    "šalį mokėtojui iš karto pateikiami mokėjimo būdai, "\
                    "kurie galimi toje šalyje. Jeigu šalis nenurodoma, "\
                    "sistema pagal mokėtojo IP adresą nustato jo šalį. "\
                    "Mokėtojui paliekama galimybė pasikeisti šalį")

    paytext = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Mokėjimo paskirtis, kuri matosi darant pavedimą")
    """
        Nenurodžius naudojamas tekstas pagal nutylėjimą:
        Apmokėjimas už prekes ir paslaugas (už nr. [order_nr]) ([site_name]).

    Jeigu nurodote mokėjimo paskirtį, būtina įtraukti šiuos kintamuosius, kurie
    galutiniame paskirties tekste bus pakeisti į atitinkamas reikšmes:

        [order_nr] - užsakymo numeris.
        [site_name] arba [owner_name] - svetainės adresas arba įmonės
        pavadinimas.

    Nenurodžius šių kintamųjų, bus naudojamas paskirties tekstas pagal
    nutylėjimą.

    Mokėjimo paskirties pavyzdys:

        Apmokėjimas už prekes pagal užsakymą [order_nr] svetainėje [site_name].
    """
    
    p_firstname = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo vardas. Pageidautina daugumoje mokėjimo būdų. "\
                    "Privaloma mokėjimą atliekant tam tikrais mokėjimo "\
                    "būdais. (pvz: mokant per PayPal)")

    p_lastname = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo pavardė. Pageidautina daugumoje mokėjimo būdų."\
                    " Privaloma mokėjimą atliekant tam tikrais mokėjimo "\
                    "būdais. (pvz: mokant per PayPal)")

    p_email = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo el. paštas privalomas. Jeigu adresas nebus "\
                    "gautas, kliento bus prašoma jį įvesti. Šiuo adresu "\
                    "mokėjimai.lt sistema informuos mokėtoją apie apmokėjimo "\
                    "būklę")

    p_street = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo adresas, kuriuo bus siunčiamos prekės (pvz: "\
                    "Mėnulio g. 7 - 7). Pageidautina. Privaloma mokėjimą "\
                    "atliekant tam tikrais mokėjimo būdais. (pvz: mokant per "\
                    "PayPal)")

    p_city = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo miestas, į kurį bus siunčiamos prekės."\
                    "(pvz: Vilnius). Pageidautina. Privaloma mokėjimą "\
                    "atliekant tam tikrais mokėjimo būdais. (pvz: mokant per "\
                    "PayPal)")

    p_state = forms.CharField(max_length=20, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo valstijos kodas (privalomas tik perkant JAV "\
                    "valstijoje). Pageidautina. Privaloma mokėjimą atliekant "\
                    "tam tikrais mokėjimo būdais. (pvz: mokant per PayPal)")

    p_zip = forms.CharField(max_length=20, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo pašto kodas. Lietuvos pašto kodus galite rasti"\
                    "<a href='http://www.post.lt/lt/?id=316'>Čia</a>. "\
                    "Pageidautina. Privaloma mokėjimą atliekant tam tikrais "\
                    "mokėjimo būdais. (pvz: mokant per PayPal)")

    p_countrycode = forms.CharField(max_length=2, required=False,
            widget=ValueHiddenInput(),
            help_text="Pirkėjo šalies kodas. Šalies sutrumpintus kodus "\
                    "galite rasti <a href='http://www.pdncommunity.com/pdn/"\
                    "board/message?board.id=prouk&message.id=398'>čia</a>. "\
                    "Pageidautina. Privaloma mokėjimą atliekant tam tikrais "\
                    "mokėjimo būdais. (pvz: mokant per PayPal)")

    sign = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Parametras, kuriuo siunčiamas duomenų parašas. Tai "\
                    "reikalinga patikrinti ar tikrai duomenys siunčiami iš "\
                    "Jūsų svetainės. Pavyzdį, kaip sugeneruoti sign reikšmę, "\
                    "galite atsisiųsti <a href='"\
                    "https://www.mokejimai.lt/f/WebToPay-Macro-Sign.zip"\
                    "'>čia<a>")

    only_payments = forms.CharField(required=False,
            widget=ValueHiddenInput(),
            help_text="Rodyti tik kablelias išskirtą mokėjimo tipų sąrašą")

    # not properly supported yet
    disallow_payments = forms.CharField(required=False,
            widget=ValueHiddenInput(),
            help_text="Nerodyti kableliais išskirto mokėjimo tipų sąrašų")

    # not properly supported yet
    charset = forms.CharField(max_length=255, required=False,
            widget=ValueHiddenInput(),
            help_text="Kokiu kodavimu užkoduoti jūsų siunčiami duomenys "\
                    "(numatytoji reikšmė utf-8)")

    repeat_request = forms.IntegerField(max_value=0, min_value=1,
            required=False,
            widget=ValueHiddenInput(),
            help_text="Jei šis parametras lygus 1, nurodoma, kad kartojamas "\
                    "ankstesnis užsakymas naudojant parametrą 'orderid'")

    test = forms.IntegerField(max_value=0, min_value=1, required=False,
            widget=ValueHiddenInput(),
            help_text="Parametras, kuriam esant galima testuoti sujungimą, "\
                    "tokiu būdu apmokėjimas nevykdomas ir rezultatas "\
                    "grąžinamas iš karto, tartum būtų sumokėta. Norint "\
                    "testuoti, būtina aktyvuoti testavimo režimą prie "\
                    "konkretaus projekto, kai prisijungiate: \"Paslaugų "\
                    "valdymas\" -> \"įmokų surinkimas\" (prie konkretaus "\
                    "projekto) -> \"Leisti testinius mokėjimus\" (pažymėkite)")

    version = forms.CharField(max_length=9, required=False,
            initial="1.4",
            widget=ValueHiddenInput(),
            help_text="Mokėjimai.lt mokėjimų sistemos specifikacijos (API) "\
                    "versijos numeris")

    def render(self):
        # Create a signed password
        if self.is_valid():
            self.sign_with_password()
            return mark_safe(u'<form action="%s" method="post">%s%s</form>' %\
                    (POSTBACK_ENDPOINT, self.as_p(), BUTTON_HTML))
        else:
            raise ValidationError(u"Errors " + self.errors.as_text())

    def sign_with_password(self): # Signs self with password
        # To be encrypted
        fields = ['projectid', 'orderid', 'lang', 'amount', 'currency',
                'accepturl', 'cancelurl', 'callbackurl', 'payment', 'country',
                'p_firstname', 'p_lastname', 'p_email', 'p_street', 'p_city',
                'p_state', 'p_zip', 'p_countrycode', 'test', 'version']
        vals = [self.cleaned_data[k] for k in f] + [WTP_PASSWORD]
        self.data.update({'sign' : Helpers.generate_ss1(vals, '')})
        self.clean() # Propagate field "sign"


class Helpers:
    @staticmethod
    def generate_ss1(values, sep):
        ret = sep.join(map(lambda x: unicode(x).strip() if x else u'', values))
        return md5(ret).hexdigest()

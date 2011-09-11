# -*- coding: utf-8 -*-

from django.db import models

from webtopay.signals import payment_was_successful, payment_was_flagged

class WebToPayResponse(models.Model):
    # Non-webtopay params

    def __unicode__(self):
        return "%s %.2f" % (self.currency, self.amount / 100)

    query = models.TextField(blank=True)
    ipaddress = models.IPAddressField(blank=True)
    flag = models.BooleanField(blank=True, default=False)
    flag_info = models.TextField(blank=True)

    # The thing we got from server
    projectid = models.BigIntegerField(null=True,
            help_text="Unikalus projekto numeris. "+\
                    "Tik patvirtinti projektai gali priimti įmokas")
    orderid = models.CharField(max_length=40,
            help_text="Užsakymo numeris iš jūsų sistemos")
    lang = models.CharField(max_length=3, blank=True,
            help_text="Galima nurodyti naudotojo kalbą, jeigu tokios kalbos "+\
                    "mokėjimai.lt nepalaiko bus parinkta kalba pagal "+\
                    "lankytojo IP adresą arba anglų kalba pagal nutylėjimą. "+\
                    "(LIT, LAV, EST, RUS, ENG, GER, POL)")
    amount = models.BigIntegerField(null=True,
            help_text="Suma centais, kurią klientas turi apmokėti")
    currency = models.CharField(max_length=3,
            help_text="Mokėjimo valiuta (LTL, USD, EUR), kuria pageidaujate, "+\
                    "kad klientas mokėtų. Jeigu nurodyta valiuta per "+\
                    "pasirinktą mokėjimo būdą negali būti priimta, "+\
                    "sistema automatiškai pagal dienos kursą konvertuos "+\
                    "į palaikomą valiutą. Atsakyme į Jūsų svetainę bus "+\
                    "paduoti payamount ir paycurrency")
    payment = models.CharField(max_length=20,
            help_text="Mokėjimo būdas. Parametras, kuriame nieko nenurodoma "+\
                    "(paliekamas tuščias). Naudotojui bus pateikta lentelė "+\
                    "su mokėjimo būdų sąrašu, pasirinkimui. Jis naudojamas "+\
                    "tik tuo atveju, jeigu norima, kad mokėjimas būtų "+\
                    "atliktas tik per konkretų mokėjimo būdą")
    country = models.CharField(max_length=2,
            help_text="Mokėtojo šalis (LT, EE, LV, GB, PL, DE). Nurodžius "+\
                    "šalį, mokėtojui iš karto pateikiami mokėjimo būdai, "+\
                    "galimi toje šalyje. Jeigu šalis nenurodoma, sistema "+\
                    "pagal mokėtojo IP adresą nustato jo šalį. Mokėtojui "+\
                    "paliekama galimybė pasikeisti šalį")
    paytext = models.TextField(
            help_text="Mokėjimo paskirtis, kuri matosi darant pavedimą.")
    _ss2 = models.CharField(blank=True, max_length=255,
            help_text="Parametras, kurio pagalba yra tikrinama, ar iš mūsų "+\
                    "serverio gavote atsakymą. Tai aukščiausio patikimumo "+\
                    "lygio tikrinimo būdas. Atsisiųskite skripto pavyzdį")
    _ss1 = models.CharField(blank=True, max_length=64,
            help_text="Parametras, kurio pagalba yra tikrinama, ar iš mūsų "+\
                    "serverio gavote atsakymą. Tai -- žemesnio nei _ss2 "+\
                    "patikimumo lygio tikrinimo būdas. Atsisiųskite pavyzdį")
    name = models.CharField(max_length=255, blank=True,
            help_text="Mokėtojo vardas, gautas iš mokėjimo sistemos. "+\
                    "Siunčiamas tik jeigu mokėjimo sistema tokį suteikia")
    surename = models.CharField(max_length=255, blank=True,
            help_text="Mokėtojo pavardė, gauta iš mokėjimo sistemos. "+\
                    "Siunčiamas tik jeigu mokėjimo sistema tokį suteikia")
    status = models.CharField(max_length=255, editable=False,
            help_text="Mokėjimo būklė: "+\
                    "0 - apmokėjimas neįvyko, "+\
                    "1 - apmokėta sėkmingai, "+\
                    "2 - mokėjimo nurodymas priimtas, bet dar neįvykdytas")

    # Error codes are stored separately
    error = models.CharField(max_length=20, blank=True,
            help_text="Klaidos kodas")

    test = models.SmallIntegerField(choices=((0, 'Production'), (1, 'Test')),
            null=True,
            help_text="Parametras, kuriam esant galima testuoti sujungimą, "+\
                    "tokiu būdu apmokėjimas nevykdomas ir rezultatas "+\
                    "grąžinamas iš karto, tartum būtų sumokėta. Norint "+\
                    "testuoti, būtina aktyvuoti testavimo režimą prie "+\
                    "konkretaus projekto, kai prisijungiate: \"Paslaugų "+\
                    "valdymas\" -> \"įmokų surinkimas\" (prie konkretaus "+\
                    "projekto) -> \"Leisti testinius mokėjimus\" (pažymėkite)")

    # In API 1.4, this field has zero allowed length, therefore textfield...
    p_email = models.TextField(
            help_text="Pirkėjo el. paštas privalomas. Jeigu adresas nebus "+\
                    "gautas, kliento bus prašoma jį įvesti. Šiuo adresu "+\
                    "mokėjimai.lt sistema informuos mokėtoją apie apmokėjimo"+\
                    " būklę")
    requestid = models.CharField(max_length=40, blank=True,
            help_text="Tai užklausos numeris, kurį gauname, kai žmogus "+\
                    "nuspaudžia ant banko ir kurį pateikiame į "+\
                    "\"callbackurl\" laukelyje nurodytą nuorodą")
    payamount = models.IntegerField(null=True,
            help_text="Suma centais, kurią pervedė. Gali skirtis jeigu buvo"+\
                    "konvertuota į kitą valiutą")

    # This is suspicious. According to the spec, its max length is 0. So in
    # theory, it should be a text field.
    paycurrency = models.CharField(max_length=10,
            help_text="Mokėjimo valiuta (LTL, USD, EUR), kurią pervedė. Gali "+\
                    "skirtis nuo tos kurios prašėte, jeigu pasirinktas "+\
                    "mokėjimo būdas negalėjo priimti prašomos valiutos")
    version = models.CharField(max_length=9,
            help_text="Mokėjimai.lt mokėjimų sistemos specifikacijos (API) "+\
                    "versijos numeris")

    """
        0x1 - Mokėjimo suma per maža
        0x2 - Mokėjimo suma per didelė
        0x3 - Nurodyta valiuta neaptarnaujama
        0x4 - Nėra sumos arba valiutos
        0x6 - Neįrašytas projectID arba tokio ID nėra
        0x7 - Išjungtas testavimo rėžimas, tačiau mėginote atlikti testinį mokėjimą
        0x8 - Jūs uždraudėte šį mokėjimo būdą
        0x9 - Blogas "paytext" kintamojo kodavimas (turi būti utf-8)
        0x10 - Tuščias arba neteisingai užpildytas "orderID"
        0x11xError - Toks projektas neegzistuoja
        0x11x0 - Projektas nėra patikrintas mūsų administratoriaus
        0x11x2 - Projektas yra sustabdytas kliento
        0x11x4 - Projektas yra blokuotas mūsų administratoriaus
        0x11x5 - Projektas yra ištrintas iš mūsų sistemos
        0x12 - Negautas projectid (projekto numeris) parametras, nors jis yra privalomas
        0x13 - Accepturl, cancellurl, callbacurl arba referer bazinis adresas skiriasi nuo projekte patvirtintų adresų
        0x14 - Klaidingas "sign" parametras
        0x15 - Klaidingi kai kurie iš perduotų parametrų
        0x15x0 - Neteisingas vienas iš šių parametrų: cancelurl, accepturl, callbackurl
    """

    def set_flag(self, info):
        self.flag = True
        self.flag_info += info

    def send_signals(self):
        if self.flag:
            payment_was_flagged.send(sender=self)
        else:
            payment_was_successful.send(sender=self)

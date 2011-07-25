from django.conf import settings

# Mandatory part
try:
    WTP_PASSWORD = settings.WEBTOPAY_PASSWORD
except:
    raise WebToPaySettingsError("Please provide WEBTOPAY_PASSWORD to settings")

CHECK_SS1 = getattr(settings, 'WEBTOPAY_CHECK_SS1', True)
CHECK_SS2 = getattr(settings, 'WEBTOPAY_CHECK_SS2', True)

BUTTON_HTML = getattr(settings, 'WEBTOPAY_BUTTON_HTML',\
        u"<input type='submit' value='Pay'/>")

POSTBACK_ENDPOINT = getattr(settings, "WEBTOPAY_POSTBACK_ENDPOINT",\
        "https://www.mokejimai.lt/pay/")

class WebToPaySettingsError(Exception):
    "Raised when WebToPay settings are incorrect"

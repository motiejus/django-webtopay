from django.conf import settings

class WebToPaySettingsError(Exception):
    "Raised when WebToPay settings are incorrect"

# Mandatory part
try:
    WTP_PASSWORD = settings.WEBTOPAY_PASSWORD
except:
    raise WebToPaySettingsError("Please provide WEBTOPAY_PASSWORD to settings")

CHECK_SS1 = getattr(settings, 'WEBTOPAY_CHECK_SS1', True)
CHECK_SS2 = getattr(settings, 'WEBTOPAY_CHECK_SS2', True)

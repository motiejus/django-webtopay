from django.conf import settings

class WebToPaySettingsError(Exception):
    """Raised when settings are bad."""


# API Endpoints. Yadda yadda.

# Various settings. Are they necessary at all?
PROJECT_ID = getattr(settings, "WEBTOPAY_PROJECT_ID", 0)
TEST = int(bool(getattr(settings, "WEBTOPAY_TEST", 0)))

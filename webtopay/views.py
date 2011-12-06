import logging
log = logging.getLogger(__name__)

from django.core.signals import got_request_exception

from django.http import HttpResponse
from django.views.decorators.http import require_GET

from webtopay.forms import WebToPayResponseForm
from webtopay.models import WebToPayResponse


def _respond_error(request, err):
    return _respond(WebToPayResponse(), request, err)

def _respond(obj, request, err=None):
    err and obj.set_flag(err)

    obj.query = request.GET.urlencode()
    obj.ipaddress = request.META.get('REMOTE_ADDR', '')
    obj.save()
    try:
        obj.send_signals()
    except:
        log.exception("Error processing response")
    return HttpResponse("OK")

@require_GET
def makro(request):
    form = WebToPayResponseForm(request.META['QUERY_STRING'])

    if not form.is_valid():
        return _respond_error(request, "Invalid form. (%s)" % form.errors)

    err = form.badly_authorizes()
    if err:
        return _respond_error(request, "Unauthorized transaction: %s" % err)

    # Form validated fine, we can try to "save" it --
    # get instance of WebToPayResponse
    try:
        resp_obj = form.save(commit=False)
    except Exception, e:
        return _respond_error(request, "Exception while processing (%s)" % e)

    return _respond(resp_obj, request)

from django.conf.urls.defaults import *

urlpatterns = patterns('webtopay.views',
    url(r'^$', 'makro', name="webtopay-makro"),
)

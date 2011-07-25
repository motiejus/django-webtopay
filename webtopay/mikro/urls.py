from django.conf.urls.defaults import *

urlpatterns = patterns('webtopay.views',
    url(r'^$', 'mikro', name="webtopay-mikro"),
)

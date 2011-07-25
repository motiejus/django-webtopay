from django.conf.urls.defaults import patterns, url, handler404, handler500

urlpatterns = patterns('webtopay.views',
    url(r'^$', 'mikro', name="webtopay-mikro"),
)

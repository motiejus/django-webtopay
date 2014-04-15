import django

if django.VERSION >= (1, 6):
    from django.conf.urls import patterns, url
else:
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('webtopay.views',
    url(r'^$', 'makro', name="webtopay-makro"),
)

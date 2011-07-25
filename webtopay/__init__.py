__version__ = (0, 0, 1)

class makro:
    class urls:
        from django.conf.urls.defaults import patterns, url,\
                handler404, handler500

        urlpatterns = patterns('webtopay.views',
            url(r'^$', 'makro', name="webtopay-makro"),
        )

class mikro:
    class urls:
        from django.conf.urls.defaults import patterns, url,\
                handler404, handler500

        urlpatterns = patterns('webtopay.views',
            url(r'^$', 'mikro', name="webtopay-mikro"),
        )

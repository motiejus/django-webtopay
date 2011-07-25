#!/usr/bin/env python
import sys

from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        ROOT_URLCONF='webtopay.urls.makro',
        INSTALLED_APPS=['webtopay'],
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3'
                }
            },
        WEBTOPAY_PASSWORD='1c4196d0ff7fe4e94bdca98fb251bc25'
    )

from django.test.simple import DjangoTestSuiteRunner

def runtests(*args):
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    testrunner = DjangoTestSuiteRunner()
    if not args:
        args = None
    failures = testrunner.run_tests(args)
    sys.exit(failures)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    runtests(*sys.argv[1:])

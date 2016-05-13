#!/usr/bin/env python
import sys

from os.path import dirname, abspath

import django
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

if django.VERSION >= (1, 8):
    from django.test.runner import DiscoverRunner as DjangoTestRunner
    django.setup()
else:
    from django.test.simple import DjangoTestSuiteRunner as DjangoTestRunner

def runtests(*args):
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    testrunner = DjangoTestRunner()
    if not args:
        args = None
    failures = testrunner.run_tests(args)
    sys.exit(failures)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    runtests(*sys.argv[1:])

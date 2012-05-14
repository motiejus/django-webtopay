# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages

import webtopay

setup(
    name='django-webtopay',
    version=".".join(map(str, webtopay.__version__)),
    author='Motiejus Jakštys',
    author_email='desired.mta@gmail.com',
    url='https://github.com/Motiejus/django-webtopay',
    install_requires=['Django>=1.3', 'M2crypto'],
    description = 'A pluggable Django application for integrating WebToPay Payments',
    packages=find_packages(),
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT"
    ],
)

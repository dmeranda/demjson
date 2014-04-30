# Python package setup script        -*- coding: utf-8 -*-

name = 'demjson'
version = '2.0'

import sys
if sys.version_info.major >= 3:
    # Python 3, use setuptools first
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup
else:
    # Python 2, use distutils first
    try:
        from distutils.core import setup
    except ImportError:
        from setuptools import setup

py3extra = {}

if sys.version_info.major >= 3:
    py3extra['use_2to3'] = True
    #py3extra['convert_2to3_doctests'] = ['src/your/module/README.txt']
    #py3extra['use_2to3_fixers'] = ['your.fixers']

setup( name=name,
       version=version,
       py_modules=[name],
       scripts=['jsonlint'],
       author='Deron Meranda',
       author_email='deron.meranda@gmail.com',
       url='http://deron.meranda.us/python/%s/'%name,
       download_url='http://deron.meranda.us/python/%(name)s/dist/%(name)s-%(version)s.tar.gz'\
           % {'name':name, 'version':version},
       description='encoder, decoder, and lint/validator for JSON (JavaScript Object Notation) compliant with RFC 7158',
       long_description="""

This module provides classes and functions for encoding or decoding data
represented in the language-neutral JSON format (which is often used as a
simpler substitute for XML in Ajax web applications).  This implementation tries
to be as compliant to the JSON specification (RFC 7158) as possible, while
still providing many optional extensions to allow less restrictive JavaScript
syntax.  It includes complete Unicode support, including UTF-32, BOM, and
surrogate pair processing.  It can also support JavaScript's
NaN and Infinity numeric types as well as it's 'undefined' type.
It also includes a lint-like JSON syntax validator which tests JSON text
for strict compliance to the standard.

""".strip(),
       license='GNU LGPL 3.0',
       keywords=['JSON','jsonlint','JavaScript','UTF-32'],
       platforms=[],
       classifiers=["Development Status :: 5 - Production/Stable",
                    "Intended Audience :: Developers",
                    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                    "Operating System :: OS Independent",
                    "Programming Language :: Python :: 2",
                    "Programming Language :: Python :: 3",
                    "Topic :: Software Development :: Libraries :: Python Modules",
                    "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
                    ],
       **py3extra
       )


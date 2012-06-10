# -*- python -*-
from distutils.core import setup
name = 'demjson'
version = '1.5'
setup( name=name,
       version=version,
       py_modules=[name],
       author='Deron Meranda',
       author_email='deron.meranda@gmail.com',
       url='http://deron.meranda.us/python/%s/'%name,
       download_url='http://deron.meranda.us/python/%(name)s/dist/%(name)s-%(version)s.tar.gz'\
           % {'name':name, 'version':version},
       description='encoder, decoder, and lint/validator for JSON (JavaScript Object Notation) compliant with RFC 4627',
       long_description="""This module provides classes and functions for encoding or decoding data
        represented in the language-neutral JSON format (which is often used as a
        simpler substitute for XML in Ajax web applications).  This implementation tries
        to be as compliant to the JSON specification (RFC 4627) as possible, while
        still providing many optional extensions to allow less restrictive JavaScript
        syntax.  It includes complete Unicode support, including UTF-32, BOM, and
        surrogate pair processing.  It can also support JavaScript's
        NaN and Infinity numeric types as well as it's 'undefined' type.
        It also includes a lint-like JSON syntax validator which tests JSON text
        for strict compliance to the standard.""",
       license='GNU LGPL 3.0',
       keywords=['JSON','jsonlint','JavaScript','UTF-32'],
       platforms=[],
       classifiers=['Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
                    ]
       )


demjson
=======

MORE DOCUMENTATION IS IN THE "docs" SUBDIRECTORY.

'demjson' is a Python language module for encoding, decoding, and
syntax-checking JSON data.


It attempts to be as closely conforming to the JSON specification,
published as IETF RFC 7158 <http://www.ietf.org/rfc/rfc7158.txt>, as
possible.  It can also be used in a non-strict mode where it is much
closer to the JavaScript/ECMAScript syntax (published as ECMA 262).
The demjson module has full Unicode support and can deal with very
large numbers.

It comes with a <b>jsonlint</b> tool which can be used to validate
your JSON documents for strict conformance to the RFC specification;
as it can also reformat them, either by re-indenting or removing
unnecessary whitespace for minimal/canonical JSON output.


Why use demjson rather than the Python standard library?
========================================================

demjson was written before Python had any built-in JSON support in its
standard library.  At the time there were just a handful of
third-party libraries; and none of them were completely compliant with
the RFC.  Also what I considered to be the best of the group
(simplejson) was a compiled C extension.

So I wrote demjson to be:

 * Pure Python, requiring no compiled extension.
 * 100% RFC compliant. It should follow the JSON specification exactly.

It should be noted that Python has since added JSON into its standard
library (which was actually an "absorption" of simplejson, the C
extension module I previously mentioned, but after it had been fixed
to repair its RFC issues).

For MOST uses, the standard Python JSON library should be sufficient.

However demjson may still be useful:

 * It works in old Python versions that don't have JSON built in;

 * It generally has better error handling and "lint" checking capabilities;

 * It can correctly deal with different Unicode encodings, including ASCII.

 * It generates more conservative JSON, such as escaping Unicode
   format control characters or line terminators, which should improve
   data portability.

 * In non-strict mode it can also deal with slightly non-conforming
   input that is more JavaScript than JSON (such as allowing comments).

 * It supports a broader set of types during conversion, including
   Python's Decimal or UserString.


Compatibility
=============

REQUIRES PYTHON 2.3 OR HIGHER, DOES NOT WORK IN PYTHON 3000 (3.x)


Installation
============
To install, type:

   python setup.py install

or optionally just copy the file "demjson.py" to whereever you want.
See docs/INSTALL.txt for mo detailed instructions.


In addition to the module "demjson", there is also an included script
"jsonlint" which is meant to be used as a command-line tool.  You can
invoke "jsonlint --help" for its usage instructions.


Documentation
=============
The module is self-documented, so within the python interpreter type:

   import demjson
   help(demjson)

or from a command line:

   pydoc demjson


Running self tests
==================
To run the accompaning self-tests, under the test/ subdirectory, do:

   cd test
   PYTHONPATH=.. python test_demjson.py


License
=======
This software is Free Software and is licensed under the terms of the
GNU LGPL (GNU Lesser General Public License).  More information is
found at the top of the demjson.py source file and the included
LICENSE.txt file.


More information
================
See the files under the "docs" subdirectory.

Complete documentation and additional information is available on the
project homepage at http://deron.meranda.us/python/demjson/

It is also available on the Python Package Index at
http://pypi.python.org/pypi/demjson/


Author
======
Written by Deron Meranda
http://deron.meranda.us/python/demjson/

demjson
=======

<b>demjson</b> is a [Python language](http://python.org/) module for
encoding, decoding, and syntax-checking [JSON](http://json.org/)
data.

It attempts to be as closely conforming to the JSON specification,
published as [IETF RFC 4627](http://www.ietf.org/rfc/rfc4627.txt), as
possible.  It can also be used in a non-strict mode where it is much
closer to the JavaScript/ECMAScript syntax (published as ECMA 262).
The demjson module has full Unicode support and can deal with very
large numbers.

It comes with a <b>jsonlint</b> tool which can be used to validate
your JSON documents for strict conformance to the RFC specification;
as it can also reformat them, either by re-indenting or removing
unnecessary whitespace for minimal/canonical JSON output.


More information
================
Complete documentation and additional information is available on the
[demjson project homepage](http://deron.meranda.us/python/demjson/).

It is also available on the
[Python Package Index](http://pypi.python.org/pypi/demjson/),
and can be installed using the Python distutils <em>easy_install</em> command.

License
=======
Versions since 1.4 or newer are LGPLv3 (GNU Lesser General Public
License, version 3 or greater).  For older versions see the
LICENSE.txt file in the source distribution.

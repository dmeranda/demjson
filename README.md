demjson
=======

<b>demjson</b> is a [Python language](http://python.org/) module for
encoding, decoding, and syntax-checking [JSON](http://json.org/)
data.

It attempts to be as closely conforming to the JSON specification,
published as [IETF RFC 7158](http://www.ietf.org/rfc/rfc7158.txt), as
possible.  It can also be used in a non-strict mode where it is much
closer to the JavaScript/ECMAScript syntax (published as ECMA 262).
The demjson module has full Unicode support and can deal with very
large numbers.

It comes with a <b>jsonlint</b> tool which can be used to validate
your JSON documents for strict conformance to the RFC specification;
as it can also reformat them, either by re-indenting or removing
unnecessary whitespace for minimal/canonical JSON output.


Why demjson?
============
demjson was written before Python had any built-in JSON support in its
standard library.  At the time there were just a handful of
third-party libraries; and none of them were completely compliant with
the RFC.  Also what I considered to be the best of the group
(simplejson) was a compiled C extension.

So I wrote demjson to be:

 * Pure Python, requiring no compiled extension
 * RFC compliant. It should follow the JSON specification exactly.

It should be noted that Python has since gotten JSON into its standard
library (which was actually an "absorption" of simplejson, the C
extension module I previously mentioned, but after it had been fixed
to repair its RFC issues).

For MOST uses, the standard Python JSON library should be sufficient.

However demjson may still be useful. In particular it in general has
better error handling and "lint" checking capabilities.


More information
================
Complete documentation and additional information is available on the
[demjson project homepage](http://deron.meranda.us/python/demjson/).

It is also available on the
[Python Package Index](http://pypi.python.org/pypi/demjson/).

License
=======
Versions since 1.4 or newer are LGPLv3 (GNU Lesser General Public
License, version 3 or greater).  For older versions see the
LICENSE.txt file in the source distribution.

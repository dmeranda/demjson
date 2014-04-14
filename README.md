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


What's new
==========

These are the changes from 1.6 to 1.7 (released 2014-04-13).  See the
file "docs/CHANGES.txt" for a complete history of changes.

 * RFC 7159 support. The new RFC (published March 2104 and which
   superseded RFC 4627) relaxes the constraint that a JSON document
   must start with an object or array.  Now any JSON value type is a
   legal JSON document.

 * Python 3. This version supports both Python 2 and Python 3, via the
   2to3 conversion program.  When installing via setup.py or a PyPI
   distribution mechanism, this conversion should automatically
   happern.

   Note that the API under Python 3 will be slightly different.
   Mainly there will be some cases in which byte array types are used
   or returned rather than strings.

   Read the file "docs/PYTHON3.txt" for complete information.

 * Unicode: When outputting JSON certain additional characters in
   strings will now always be \u-escaped to increase compatibility
   with JavaScript.  This includes line terminators (which are
   forbidden in JavaScript string literals) as well as format control
   characters (which any JavaScript implementation is allowed to
   ignore if it chooses per the ECMAscript standard).

   This essentially means that characters in any of the Unicode
   categories of Cc, Cf, Zl, and Zp will be \u-escaped; which includes
   for example:

       - U+007F  DELETE               (Category Cc)
       - U+00AD  SOFT HYPHEN          (Category Cf)
       - U+200F  RIGHT-TO-LEFT MARK   (Category Cf)
       - U+2028  LINE SEPARATOR       (Category Zl)
       - U+2029  PARAGRAPH SEPARATOR  (Category Zp)
       - U+E007F CANCEL TAG           (Category Cf)

 * Mutable strings: Support for the old Python type
   "UserString.MutableString" type has been dropped.  That
   experimental type had already been deprecated since Python 2.6 and
   removed entirely from Python 3.  If you have code that passes a
   MutableString to a JSON encoding function then either do not
   upgrade to this release, or first convert such types to standard
   strings before JSON encoding them.

 * The "jsonlint" command script will now be installed by default.

 * jsonlint class: Almost all the logic of the jsonlint script is now
   available as a new class, demjson.jsonlint, should you want to call
   it programatically.

   The included "jsonlint" script file is now just a very small
   wrapper around that class.

 * Other jsonlint improvements:
       - Fixed bugs in reading from stdin
       - New -o option to specify output filename
       - Verbosity is on by default, new --quiet option
       - Better help text


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

However demjson may still be useful for some purposes:

 * It works in old Python versions that don't have JSON built in;

 * It generally has better error handling and "lint" checking capabilities;

 * It will automatically use the Python Decimal (bigfloat) class
   instead of a floating-point number whenever there might be an
   overflow or loss of precision otherwise.

 * It can correctly deal with different Unicode encodings, including ASCII.
   It will automatically adapt when to use \u-escapes based on the encoding.

 * It generates more conservative JSON, such as escaping Unicode
   format control characters or line terminators, which should improve
   data portability.

 * In non-strict mode it can also deal with slightly non-conforming
   input that is more JavaScript than JSON (such as allowing comments).

 * It supports a broader set of types during conversion, including
   Python's Decimal or UserString.


More information
================
See the files under the "docs" subdirectory.

Complete documentation and additional information is available on the
[demjson project homepage](http://deron.meranda.us/python/demjson/).

It is also available on the
[Python Package Index](http://pypi.python.org/pypi/demjson/).


License
=======
Versions since 1.4 or newer are LGPLv3 (GNU Lesser General Public
License, version 3 or greater).  For older versions see the
LICENSE.txt file in the source distribution.

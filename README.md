demjson
=======

<b>demjson</b> is a [Python language](http://python.org/) module for
encoding, decoding, and syntax-checking [JSON](http://json.org/)
data.  It works under both Python 2 and Python 3.

It comes with a <b>jsonlint</b> script which can be used to validate
your JSON documents for strict conformance to the JSON specification.
It can also reformat or pretty-print JSON documents; either by
re-indenting or removing unnecessary whitespace for minimal/canonical
JSON output.

demjson tries to be as closely conforming to the JSON specification,
published as [IETF RFC 7158](http://www.ietf.org/rfc/rfc7158.txt), as
possible.  It can also be used in a non-strict mode where it is much
closer to the JavaScript/ECMAScript syntax (published as ECMA 262).
The demjson module has full Unicode support and can deal with very
large numbers.


Example use
===========

To use demjson from within your Python programs:

```python
    import demjson

    # Convert a Python value into JSON
    demjson.encode( {'Happy': True, 'Other': None} )
          # returns string =>  {"Happy":true,"Other":null}

    # Convert a JSON document into a Python value
    demjson.decode( '{"Happy":true,"Other":null}' )
          # returns dict => {'Other': None, 'Happy': True}
```

To use the accompaning "jsonlint" command script:

```bash
    # To check whether a file contains valid JSON
    jsonlint sample.json

    # To pretty-print (reformat) a JSON file
    jsonlint --format sample.json
```


What's new
==========

These are the changes from 1.6 to 1.7 (released 2014-04-13).  See the
file "docs/CHANGES.txt" for a complete history of changes.

 * Python 3: This version supports both Python 2 and Python 3, via the
   2to3 conversion program.  When installing with setup.py or a PyPI
   distribution mechanism such as pip or easy_install, this conversion
   should automatically happen.

   Note that the API under Python 3 will be slightly different.
   Mainly new Python types are supported.  Also there will be some
   cases in which byte array types are used or returned rather than
   strings.

   Read the file "docs/PYTHON3.txt" for complete information.

 * RFC 7159 conformance: The new RFC (published March 2014 and which
   superseded RFC 4627) relaxes the constraint that a JSON document
   must start with an object or array.  This also brings it into
   alignment with the ECMA-404 standard.

   Now any JSON value type is a legal JSON document.

 * Callback hooks: This version allows the user to provide a number
   of different callback functions, or hooks, which can do special
   processing.  For example when parsing JSON you could detect
   strings that look like dates, and automatically convert them
   into Python datetime objects instead.

   Read the file "docs/HOOKS.txt" for complete information.

 * Subclassing: Subclassing the demjson.JSON class is now highly
   discouraged as future changes may alter the method parameters or names.

   In particular overriding the encode_default() method is now
   DEPRECATED!  It will continue work in this version, but will be
   removed in a future version.

   The new callback hooks (see below) should provide a better way to
   achieve most needs that previously would have been done with
   subclassing.

 Data type support
 -----------------

 * Python 3 types: Many new types introduced with Python 3 are
   directly supported, when running in a Python 3 environment.  This
   includes 'bytes', 'bytearray', 'memoryview', and 'ChainMap'.

   Read the file "docs/PYTHON3.txt" for complete information.

 * Named tuples: When encoding to JSON, all named tuples (objects of
   Python's standard 'collections.namedtuple' type) are now encoded
   into JSON as objects rather than as arrays.  This behavior can be
   changed with the 'encode_namedtuple_as_object' argument to False,
   in which case they will be treated as a normal tuple.

```python
       from collections import namedtuple
       Point = namedtuple('Point', ['x','y'])
       p = Point(5, 8)

       demjson.encode( p )
            # gives =>    {"x":5, "y":8}

       demjson.encode( p, encode_namedtuple_as_object=False )
            # gives =>    [5, 8]
```

   This behavior also applies to any object that follows the
   namedtuple protocol, i.e., which are subclasses of 'tuple' and that
   have an "_asdict()" method.

   Note that the order of keys is not necessarily preserved, but instead
   will appear in the JSON output alphabetically.

 * Mutable strings: Support for the old Python mutable strings (the
   UserDict.MutableString type) has been dropped.  That experimental
   type had already been deprecated since Python 2.6 and removed
   entirely from Python 3.  If you have code that passes a
   MutableString to a JSON encoding function then either do not
   upgrade to this release, or first convert such types to standard
   strings before JSON encoding them.

 Unicode and codec support
 -------------------------

 * Codecs: The 'encoding' argument to the decode() and encode()
   functions will now accept a codec object as well as an encoding
   name; i.e., any subclass of 'codecs.CodecInfo'.  All \u-escaping in
   string literals will be automatically adjusted based on your custom
   codec's repertoire of characters.

 * UTF-32: The included functions for UTF-32/UCS-4 support (missing
   from older versions of Python) are now presented as a full-blown
   codec class: 'demjson.utf32'.  It is completely compatible with the
   standard codecs module.

   It is normally unregisted, but you may register it with the Python codecs system by:

```python
       import demjson, codecs
       codecs.register( demjson.utf32.lookup )
```

 * Unicode errors: During reading or writing JSON as raw bytes (when
   an encoding is specified), any Unicode errors are now wrapped in a
   JSON error instead.

       - UnicodeDecodeError is transformed into JSONDecodeError
       - UnicodeEncodeError is transformed into JSONEncodeError

   When running in Python 3 the standard Exception Chaining (PEP 3134)
   mechanism is employed.  Under Python 2 exception chaining is
   simulated, but a printed traceback of the original exception may
   not be printed. You can get to the original exception in the
   __cause__ member of the outer exception.

 * Unicode escapes: When outputting JSON certain additional characters
   in strings will now always be \u-escaped to increase compatibility
   with JavaScript.  This includes line terminators (which are
   forbidden in JavaScript string literals) as well as format control
   characters (which any JavaScript implementation is allowed to
   ignore if it chooses per the ECMAscript standard).

   This essentially means that characters in any of the Unicode
   categories of Cc, Cf, Zl, and Zp will always be \u-escaped; which
   includes for example:

       - U+007F  DELETE               (Category Cc)
       - U+00AD  SOFT HYPHEN          (Category Cf)
       - U+200F  RIGHT-TO-LEFT MARK   (Category Cf)
       - U+2028  LINE SEPARATOR       (Category Zl)
       - U+2029  PARAGRAPH SEPARATOR  (Category Zp)
       - U+E007F CANCEL TAG           (Category Cf)

 Errors and warnings
 -------------------

 * Error types: The base error type 'JSONError' is now a subclass of
   Python's standard 'Exception' class rather than 'ValueError'.  If
   you had been using try...except blocks with ValueError then you
   will need to change; preferably to catch JSONError.

 jsonlint command
 ----------------

 * The "jsonlint" command script will now be installed by default.

 * jsonlint class: Almost all the logic of the jsonlint script is now
   available as a new class, demjson.jsonlint, should you want to call
   it programatically.

   The included "jsonlint" script file is now just a very small
   wrapper around that class.

 * Other jsonlint improvements:
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

For most uses, the standard Python JSON library should be sufficient.

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


Installation
============

To install, type:

```bash
   python setup.py install
```

or optionally just copy the file "demjson.py" to whereever you want.
See "docs/INSTALL.txt" for more detailed instructions, including how
to run the self-tests.


More information
================

See the files under the "docs" subdirectory.  The module is also
self-documented, so within the python interpreter type:

```python
    import demjson
    help(demjson)
```

or from a shell command line:

```bash
    pydoc demjson
```

The "jsonlint" command script which gets installed as part of demjson
has built-in usage instructions as well.  Just type:

```bash
   jsonlint --help
```

Complete documentation and additional information is also available on
the project homepage at http://deron.meranda.us/python/demjson/

It is also available on the Python Package Index (PyPI) at
http://pypi.python.org/pypi/demjson/


License
=======

LGPLv3 - See the included "LICENSE.txt" file.

This software is Free Software and is licensed under the terms of the
GNU LGPL (GNU Lesser General Public License).  More information is
found at the top of the demjson.py source file and the included
LICENSE.txt file.

Releases prior to 1.4 were released under a different license, be
sure to check the corresponding LICENSE.txt file included with them.

This software was written by Deron Meranda, http://deron.meranda.us/

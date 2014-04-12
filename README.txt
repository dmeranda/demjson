demjson
=======

'demjson' is a Python language module for encoding, decoding, and
syntax-checking JSON data.

Additional documentation may be found under the "docs/" directory.


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


License
=======
This software is Free Software and is licensed under the terms of the
GNU LGPL (GNU Lesser General Public License).  More information is
found at the top of the demjson.py source file and the included
LICENSE.txt file.


Author
======
Written by Deron Meranda
http://deron.meranda.us/python/demjson/

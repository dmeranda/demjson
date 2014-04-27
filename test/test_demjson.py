#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module tests demjson.py using unittest.

NOTE ON PYTHON 3: If running in Python 3, you must transform this test
                  script with "2to3" first.

"""

import sys, os, time
import unittest
import string
import unicodedata
import collections
import datetime

# Force PYTHONPATH to head of sys.path, as the easy_install (egg files) will
# have rudely forced itself ahead of PYTHONPATH.

for pos, name in enumerate(os.environ.get('PYTHONPATH','').split(os.pathsep)):
    if os.path.isdir(name):
        sys.path.insert(pos, name)

import demjson

# ------------------------------
# Python version-specific stuff...

is_python3 = (sys.version_info.major >= 3)

if hasattr(unittest, 'skipUnless'):
    def skipUnlessPython3(method):
        return unittest.skipUnless(method, is_python3)
else:
    # Python <= 2.6 does not have skip* decorators, so
    # just make a dummy decorator that always passes the
    # test method.
    def skipUnlessPython3(method):
        def always_pass(self):
            print "\nSKIPPING TEST %s: Requires Python 3" % method.__name__
            return True
        return always_pass

## ------------------------------

def rawbytes( byte_list ):
    if is_python3:
        b = bytes( byte_list )
    else:
        b = ''.join(chr(n) for n in byte_list)
    return b

## ------------------------------

try:
    import UserDict
    dict_mixin = UserDict.DictMixin
except ImportError:
    # Python 3 has no UserDict. MutableMapping is close, but must
    # supply own __iter__() and __len__() methods.
    dict_mixin = collections.MutableMapping

# A class that behaves like a dict, but is not a subclass of dict
class LetterOrdDict(dict_mixin):
    def __init__(self, letters):
        self._letters = letters
    def __getitem__(self,key):
        try:
            if key in self._letters:
                return ord(key)
        except TypeError:
            raise KeyError('Key of wrong type: %r' % key)
        raise KeyError('No such key', key)
    def __setitem__(self,key): raise RuntimeError('read only object')
    def __delitem__(self,key): raise RuntimeError('read only object')
    def keys(self):
        return list(self._letters)
    def __len__(self):
        return len(self._letters)
    def __iter__(self):
        for v in self._letters:
            yield v

## ------------------------------

if is_python3:
    def hexencode_bytes( bytelist ):
        return ''.join( ['%02x' % n for n in bytelist] )

## ============================================================

class DemjsonTest(unittest.TestCase):
    """This class contains test cases for demjson.

    """
    def testConstants(self):
        self.failIf( not isinstance(demjson.nan, float), "Missing nan constant" )
        self.failIf( not isinstance(demjson.inf, float), "Missing inf constant" )
        self.failIf( not isinstance(demjson.neginf, float), "Missing neginf constant" )
        self.failIf( not hasattr(demjson, 'undefined'), "Missing undefined constant" )

    def testDecodeKeywords(self):
        self.assertEqual(demjson.decode('true'), True)
        self.assertEqual(demjson.decode('false'), False)
        self.assertEqual(demjson.decode('null'), None)
        self.assertEqual(demjson.decode('undefined'), demjson.undefined)

    def testEncodeKeywords(self):
        self.assertEqual(demjson.encode(None), 'null')
        self.assertEqual(demjson.encode(True), 'true')
        self.assertEqual(demjson.encode(False), 'false')
        self.assertEqual(demjson.encode(demjson.undefined), 'undefined')

    def testDecodeNumber(self):
        self.assertEqual(demjson.decode('0'), 0)
        self.assertEqual(demjson.decode('12345'), 12345)
        self.assertEqual(demjson.decode('-12345'), -12345)
        self.assertEqual(demjson.decode('1e6'), 1000000)
        self.assertEqual(demjson.decode('1.5'), 1.5)
        self.assertEqual(demjson.decode('-1.5'), -1.5)
        self.assertEqual(demjson.decode('3e10'), 30000000000)
        self.assertEqual(demjson.decode('3E10'), 30000000000)
        self.assertEqual(demjson.decode('3e+10'), 30000000000)
        self.assertEqual(demjson.decode('3E+10'), 30000000000)
        self.assertEqual(demjson.decode('3E+00010'), 30000000000)
        self.assertEqual(demjson.decode('1000e-2'), 10)
        self.assertEqual(demjson.decode('1.2E+3'), 1200)
        self.assertEqual(demjson.decode('3.5e+8'), 350000000)
        self.assertEqual(demjson.decode('-3.5e+8'), -350000000)
        self.assertAlmostEqual(demjson.decode('1.23456e+078'), 1.23456e78)
        self.assertAlmostEqual(demjson.decode('1.23456e-078'), 1.23456e-78)
        self.assertAlmostEqual(demjson.decode('-1.23456e+078'), -1.23456e78)
        self.assertAlmostEqual(demjson.decode('-1.23456e-078'), -1.23456e-78)

    def testDecodeStrictNumber(self):
        """Make sure that strict mode is picky about numbers."""
        for badnum in ['+1', '.5', '1.', '01', '0x1', '1e']:
            try:
                self.assertRaises(demjson.JSONDecodeError, demjson.decode, badnum, strict=True, allow_any_type_at_start=True)
            except demjson.JSONDecodeError:
                pass

    def testDecodeHexNumbers(self):
        self.assertEqual(demjson.decode('0x8', allow_hex_numbers=True), 8)
        self.assertEqual(demjson.decode('0x1f', allow_hex_numbers=True), 31)
        self.assertEqual(demjson.decode('0x1F', allow_hex_numbers=True), 31)
        self.assertEqual(demjson.decode('0xff', allow_hex_numbers=True), 255)
        self.assertEqual(demjson.decode('0xffff', allow_hex_numbers=True), 65535)
        self.assertEqual(demjson.decode('0xffffffff', allow_hex_numbers=True), 4294967295)

    def testDecodeLargeIntegers(self):
        self.assertEqual(demjson.decode('9876543210123456789'), 9876543210123456789)
        self.assertEqual(demjson.decode('-9876543210123456789'), -9876543210123456789)
        self.assertEqual(demjson.decode('0xfedcba9876543210ABCDEF', allow_hex_numbers=True), 308109520888805757320678895)
        self.assertEqual(demjson.decode('-0xfedcba9876543210ABCDEF', allow_hex_numbers=True), -308109520888805757320678895)
        self.assertEqual(demjson.decode('0177334565141662503102052746757', allow_octal_numbers=True),  308109520888805757320678895)
        self.assertEqual(demjson.decode('-0177334565141662503102052746757', allow_octal_numbers=True),  -308109520888805757320678895)

    def testDecodeOctalNumbers(self):
        self.assertEqual(demjson.decode('017', allow_octal_numbers=True), 15)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '018', allow_octal_numbers=True)

    def testDecodeNegativeZero(self):
        """Makes sure 0 and -0 are distinct.

        This is not a JSON requirement, but is required by ECMAscript.

        """
        self.assertEqual(demjson.decode('-0.0'), -0.0)
        self.assertEqual(demjson.decode('0.0'), 0.0)
        self.assert_(demjson.decode('0.0') is not demjson.decode('-0.0'),
                     'Numbers 0.0 and -0.0 are not distinct')
        self.assert_(demjson.decode('0') is not demjson.decode('-0'),
                     'Numbers 0 and -0 are not distinct')

    def assertMatchesRegex(self, value, pattern, msg=None):
        import re
        r = re.compile( '^' + pattern + '$' )
        try:
            m = r.match( value )
        except TypeError:
            raise self.failureException, \
                  "can't compare non-string to regex: %r" % value
        if m is None:
            raise self.failureException, \
                  (msg or '%r !~ /%s/' %(value,pattern))

    def testEncodeNumber(self):
        self.assertEqual(demjson.encode(0), '0')
        self.assertEqual(demjson.encode(12345), '12345')
        self.assertEqual(demjson.encode(-12345), '-12345')
        # Floating point numbers must be "approximately" compared to
        # allow for slight changes due to rounding errors in the
        # least significant digits.
        self.assertMatchesRegex(demjson.encode(1.5),
                                r'1.(' \
                                r'(5(000+[0-9])?)' \
                                r'|' \
                                r'(4999(9+[0-9])?)' \
                                r')' )
        self.assertMatchesRegex(demjson.encode(-1.5),
                                r'-1.(' \
                                r'(5(000+[0-9])?)' \
                                r'|' \
                                r'(4999(9+[0-9])?)' \
                                r')' )
        self.assertMatchesRegex(demjson.encode(1.2300456e78),
                                r'1.230045(' \
                                r'(6(0+[0-9])?)' r'|' \
                                r'(59(9+[0-9])?)' \
                                r')[eE][+]0*78')
        self.assertMatchesRegex(demjson.encode(1.2300456e-78),
                                r'1.230045(' \
                                r'(6(0+[0-9])?)' r'|' \
                                r'(59(9+[0-9])?)' \
                                r')[eE][-]0*78')
        self.assertMatchesRegex(demjson.encode(-1.2300456e78),
                                r'-1.230045(' \
                                r'(6(0+[0-9])?)' r'|' \
                                r'(59(9+[0-9])?)' \
                                r')[eE][+]0*78')
        self.assertMatchesRegex(demjson.encode(-1.2300456e-78),
                                r'-1.230045(' \
                                r'(6(0+[0-9])?)' r'|' \
                                r'(59(9+[0-9])?)' \
                                r')[eE][-]0*78')
        self.assertMatchesRegex(demjson.encode(0.0000043), r'4.3[0[0-9]*]?[eE]-0*6$')
        self.assertMatchesRegex(demjson.encode(40000000000), r'(4[eE]+0*10)|(40000000000)$',
                     'Large integer not encoded properly')

    def testEncodeNegativeZero(self):
        self.assert_(demjson.encode(-0.0) in ['-0','-0.0'],
                     'Float -0.0 is not encoded as a negative zero')

    def testDecodeString(self):
        self.assertEqual(demjson.decode(r'""'), '')
        self.assertEqual(demjson.decode(r'"a"'), 'a')
        self.assertEqual(demjson.decode(r'"abc def"'), 'abc def')
        self.assertEqual(demjson.decode(r'"\n\t\\\"\b\r\f"'), '\n\t\\"\b\r\f')
        self.assertEqual(demjson.decode(r'"\abc def"'), 'abc def')

    def testEncodeString(self):
        self.assertEqual(demjson.encode(''), r'""')
        self.assertEqual(demjson.encode('a'), r'"a"')
        self.assertEqual(demjson.encode('abc def'), r'"abc def"')
        self.assertEqual(demjson.encode('\n'), r'"\n"')
        self.assertEqual(demjson.encode('\n\t\r\b\f'), r'"\n\t\r\b\f"')
        self.assertEqual(demjson.encode('\n'), r'"\n"')
        self.assertEqual(demjson.encode('"'), r'"\""')
        self.assertEqual(demjson.encode('\\'), '"\\\\"')

    def testDecodeStringWithNull(self):
        self.assertEqual(demjson.decode('"\x00"'), '\0')
        self.assertEqual(demjson.decode('"a\x00b"'), 'a\x00b')

    def testDecodeStringUnicodeEscape(self):
        self.assertEqual(demjson.decode(r'"\u0000"'), '\0')
        self.assertEqual(demjson.decode(r'"\u0061"'), 'a')
        self.assertEqual(demjson.decode(r'"\u2012"'), u'\u2012')
        self.assertEqual(demjson.decode(r'"\u00a012"'), u'\u00a0' + '12')

    def testEncodeStringUnicodeEscape(self):
        self.assertEqual(demjson.encode('\0', escape_unicode=True), r'"\u0000"')
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=True), r'"\u00e0"')
        self.assertEqual(demjson.encode(u'\u2012', escape_unicode=True), r'"\u2012"')

    def testAutoDetectEncoding(self):
        QT = ord('"')
        TAB = ord('\t')
        FOUR = ord('4')
        TWO  = ord('2')
        # Plain byte strings, without BOM
        self.assertEqual(demjson.decode( rawbytes([ 0, 0, 0, FOUR               ]) ), 4 )  # UTF-32BE
        self.assertEqual(demjson.decode( rawbytes([ 0, 0, 0, FOUR, 0, 0, 0, TWO ]) ), 42 )

        self.assertEqual(demjson.decode( rawbytes([ FOUR, 0, 0, 0               ]) ), 4 )  # UTF-32LE
        self.assertEqual(demjson.decode( rawbytes([ FOUR, 0, 0, 0, TWO, 0, 0, 0 ]) ), 42 )

        self.assertEqual(demjson.decode( rawbytes([ 0, FOUR, 0, TWO ]) ), 42 ) # UTF-16BE
        self.assertEqual(demjson.decode( rawbytes([ FOUR, 0, TWO, 0 ]) ), 42 ) # UTF-16LE

        self.assertEqual(demjson.decode( rawbytes([ 0, FOUR ]) ), 4 )  #UTF-16BE
        self.assertEqual(demjson.decode( rawbytes([ FOUR, 0 ]) ), 4 )  #UTF-16LE

        self.assertEqual(demjson.decode( rawbytes([ FOUR, TWO ]) ), 42 )  # UTF-8
        self.assertEqual(demjson.decode( rawbytes([ TAB, FOUR, TWO ]) ), 42 ) # UTF-8
        self.assertEqual(demjson.decode( rawbytes([ FOUR ]) ), 4 ) # UTF-8

        # With byte-order marks (BOM)
        #    UTF-32BE
        self.assertEqual(demjson.decode( rawbytes([ 0, 0, 0xFE, 0xFF, 0, 0, 0, FOUR ]) ), 4 )
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ 0, 0, 0xFE, 0xFF, FOUR, 0, 0, 0 ]) )
        #    UTF-32LE
        self.assertEqual(demjson.decode( rawbytes([ 0xFF, 0xFE, 0, 0, FOUR, 0, 0, 0 ]) ), 4 )
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ 0xFF, 0xFE, 0, 0, 0, 0, 0, FOUR ]) )
        #    UTF-16BE
        self.assertEqual(demjson.decode( rawbytes([ 0xFE, 0xFF, 0, FOUR ]) ), 4 )
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ 0xFE, 0xFF, FOUR, 0 ]) )
        #    UTF-16LE
        self.assertEqual(demjson.decode( rawbytes([ 0xFF, 0xFE, FOUR, 0 ]) ), 4 )
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ 0xFF, 0xFE, 0, FOUR ]) )
        
        # Invalid Unicode strings
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ 0 ]) )
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ TAB, FOUR, TWO, 0 ]) )
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ FOUR, 0, 0 ]) )
        self.assertRaises(demjson.JSONDecodeError,
                          demjson.decode, rawbytes([ FOUR, 0, 0, TWO ]) )

    def testDecodeStringRawUnicode(self):
        QT = ord('"')
        self.assertEqual(demjson.decode(rawbytes([ QT,0xC3,0xA0,QT ]),
                                        encoding='utf-8'), u'\u00e0')
        self.assertEqual(demjson.decode(rawbytes([ QT,0,0,0, 0xE0,0,0,0, QT,0,0,0 ]),
                                        encoding='ucs4le'), u'\u00e0')
        self.assertEqual(demjson.decode(rawbytes([ 0,0,0,QT, 0,0,0,0xE0, 0,0,0,QT ]),
                                        encoding='ucs4be'), u'\u00e0')
        self.assertEqual(demjson.decode(rawbytes([ 0,0,0,QT, 0,0,0,0xE0, 0,0,0,QT ]),
                                        encoding='utf-32be'), u'\u00e0')
        self.assertEqual(demjson.decode(rawbytes([ 0,0,0xFE,0xFF, 0,0,0,QT, 0,0,0,0xE0, 0,0,0,QT ]),
                                        encoding='ucs4'), u'\u00e0')

    def testEncodeStringRawUnicode(self):
        QT = ord('"')
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ QT, 0xC3, 0xA0, QT ]) )
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='ucs4le'),
                         rawbytes([ QT,0,0,0, 0xE0,0,0,0, QT,0,0,0 ]) )
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='ucs4be'),
                         rawbytes([ 0,0,0,QT, 0,0,0,0xE0, 0,0,0,QT ]) )
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='utf-32be'),
                         rawbytes([ 0,0,0,QT, 0,0,0,0xE0, 0,0,0,QT ]) )
        self.assert_(demjson.encode(u'\u00e0', escape_unicode=False, encoding='ucs4')
                     in [rawbytes([ 0,0,0xFE,0xFF, 0,0,0,QT, 0,0,0,0xE0, 0,0,0,QT ]),
                         rawbytes([ 0xFF,0xFE,0,0, QT,0,0,0, 0xE0,0,0,0, QT,0,0,0 ]) ])

    def testEncodeStringWithSpecials(self):
        # Make sure that certain characters are always \u-encoded even if the
        # output encoding could have represented them in the raw.

        # Test U+001B escape - a control character
        self.assertEqual(demjson.encode(u'\u001B', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ ord(c) for c in '"\\u001b"' ]) )
        # Test U+007F delete - a control character
        self.assertEqual(demjson.encode(u'\u007F', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ ord(c) for c in '"\\u007f"' ]) )
        # Test U+00AD soft hyphen - a format control character
        self.assertEqual(demjson.encode(u'\u00AD', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ ord(c) for c in '"\\u00ad"' ]) )
        # Test U+200F right-to-left mark
        self.assertEqual(demjson.encode(u'\u200F', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ ord(c) for c in '"\\u200f"' ]) )
        # Test U+2028 line separator
        self.assertEqual(demjson.encode(u'\u2028', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ ord(c) for c in '"\\u2028"' ]) )
        # Test U+2029 paragraph separator
        self.assertEqual(demjson.encode(u'\u2029', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ ord(c) for c in '"\\u2029"' ]) )
        # Test U+E007F cancel tag
        self.assertEqual(demjson.encode(u'\U000E007F', escape_unicode=False, encoding='utf-8'),
                         rawbytes([ ord(c) for c in '"\\udb40\\udc7f"' ]) )

    def testDecodeSupplementalUnicode(self):
        import sys
        if sys.maxunicode > 65535:
            self.assertEqual(demjson.decode( rawbytes([ ord(c) for c in r'"\udbc8\udf45"' ]) ),
                             u'\U00102345')
            self.assertEqual(demjson.decode( rawbytes([ ord(c) for c in r'"\ud800\udc00"' ]) ),
                             u'\U00010000')
            self.assertEqual(demjson.decode( rawbytes([ ord(c) for c in r'"\udbff\udfff"' ]) ),
                             u'\U0010ffff')
        for bad_case in [r'"\ud801"', r'"\udc02"',
                         r'"\ud801\udbff"', r'"\ud801\ue000"',
                         r'"\ud801\u2345"']:
            try:
                self.assertRaises(demjson.JSONDecodeError,
                                  demjson.decode( rawbytes([ ord(c) for c in bad_case ]) ) )
            except demjson.JSONDecodeError:
                pass

    def testEncodeSupplementalUnicode(self):
        import sys
        if sys.maxunicode > 65535:
            self.assertEqual(demjson.encode(u'\U00010000',encoding='ascii'),
                             rawbytes([ ord(c) for c in r'"\ud800\udc00"' ]) )
            self.assertEqual(demjson.encode(u'\U00102345',encoding='ascii'),
                             rawbytes([ ord(c) for c in r'"\udbc8\udf45"' ]) )
            self.assertEqual(demjson.encode(u'\U0010ffff',encoding='ascii'),
                             rawbytes([ ord(c) for c in r'"\udbff\udfff"' ]) )

    def testDecodeArraySimple(self):
        self.assertEqual(demjson.decode('[]'), [])
        self.assertEqual(demjson.decode('[ ]'), [])
        self.assertEqual(demjson.decode('[ 42 ]'), [42])
        self.assertEqual(demjson.decode('[ 42 ,99 ]'), [42, 99])
        self.assertEqual(demjson.decode('[ 42, ,99 ]', strict=False), [42, demjson.undefined, 99])
        self.assertEqual(demjson.decode('[ "z" ]'), ['z'])
        self.assertEqual(demjson.decode('[ "z[a]" ]'), ['z[a]'])

    def testDecodeArrayBad(self):
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '[,]', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '[1,]', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '[,1]', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '[1,,2]', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '[1 2]', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '[[][]]', strict=True)

    def testDecodeArrayNested(self):
        self.assertEqual(demjson.decode('[[]]'), [[]])
        self.assertEqual(demjson.decode('[ [ ] ]'), [[]])
        self.assertEqual(demjson.decode('[[],[]]'), [[],[]])
        self.assertEqual(demjson.decode('[[42]]'), [[42]])
        self.assertEqual(demjson.decode('[[42,99]]'), [[42,99]])
        self.assertEqual(demjson.decode('[[42],33]'), [[42],33])
        self.assertEqual(demjson.decode('[[42,[],44],[77]]'), [[42,[],44],[77]])

    def testEncodeArraySimple(self):
        self.assertEqual(demjson.encode([]), '[]')
        self.assertEqual(demjson.encode([42]), '[42]')
        self.assertEqual(demjson.encode([42,99]), '[42,99]')
        self.assertEqual(demjson.encode([42,demjson.undefined,99]), '[42,undefined,99]')

    def testEncodeArrayNested(self):
        self.assertEqual(demjson.encode([[]]), '[[]]')
        self.assertEqual(demjson.encode([[42]]), '[[42]]')
        self.assertEqual(demjson.encode([[42, 99]]), '[[42,99]]')
        self.assertEqual(demjson.encode([[42], 33]), '[[42],33]')
        self.assertEqual(demjson.encode([[42, [], 44], [77]]), '[[42,[],44],[77]]')

    def testDecodeObjectSimple(self):
        self.assertEqual(demjson.decode('{}'), {})
        self.assertEqual(demjson.decode('{"a":1}'), {'a':1})
        self.assertEqual(demjson.decode('{ "a" : 1}'), {'a':1})
        self.assertEqual(demjson.decode('{"a":1,"b":2}'), {'a':1,'b':2})
        self.assertEqual(demjson.decode('{"a":1,"b":2,"c{":3}'), {'a':1,'b':2,'c{':3})
        self.assertEqual(demjson.decode('{"a":1,"b":2,"d}":3}'), {'a':1,'b':2,'d}':3})

    def testDecodeObjectBad(self):
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '{"a"}', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '{"a":}', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '{,"a":1}', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '{"a":1,}', strict=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '{["a","b"]:1}', strict=True)

    def testDecodeObjectNested(self):
        self.assertEqual(demjson.decode('{"a":{"b":2}}'), {'a':{'b':2}})
        self.assertEqual(demjson.decode('{"a":{"b":2,"c":"{}"}}'), {'a':{'b':2,'c':'{}'}})
        self.assertEqual(demjson.decode('{"a":{"b":2},"c":{"d":4}}'), \
                         {'a':{'b':2},'c':{'d':4}})

    def testEncodeObjectSimple(self):
        self.assertEqual(demjson.encode({}), '{}')
        self.assertEqual(demjson.encode({'a':1}), '{"a":1}')
        self.assertEqual(demjson.encode({'a':1,'b':2}), '{"a":1,"b":2}')
        self.assertEqual(demjson.encode({'a':1,'c':3,'b':'xyz'}), '{"a":1,"b":"xyz","c":3}')

    def testEncodeObjectNested(self):
        self.assertEqual(demjson.encode({'a':{'b':{'c':99}}}), '{"a":{"b":{"c":99}}}')
        self.assertEqual(demjson.encode({'a':{'b':88},'c':99}), '{"a":{"b":88},"c":99}')

    def testEncodeObjectDictLike(self):
        """Makes sure it can encode things which look like dictionarys but aren't.

        """
        letters = 'ABCDEFGHIJKL'
        mydict = LetterOrdDict( letters )
        self.assertEqual( demjson.encode(mydict),
                          '{' + ','.join(['"%s":%d'%(c,ord(c)) for c in letters]) + '}' )

    def testEncodeArrayLike(self):
        class LikeList(object):
            def __iter__(self):
                class i(object):
                    def __init__(self):
                        self.n = 0
                    def next(self):
                        self.n += 1
                        if self.n < 10:
                            return 2**self.n
                        raise StopIteration
                return i()
        mylist = LikeList()
        self.assertEqual(demjson.encode(mylist), \
                         '[2,4,8,16,32,64,128,256,512]' )

    def testEncodeStringLike(self):
        import UserString
        class LikeString(UserString.UserString):
            pass
        mystring = LikeString('hello')
        self.assertEqual(demjson.encode(mystring), '"hello"')
        mystring = LikeString(u'hi\u2012there')
        self.assertEqual(demjson.encode(mystring, escape_unicode=True, encoding='utf-8'),
                         rawbytes([ ord(c) for c in r'"hi\u2012there"' ]) )

    def testObjectNonstringKeys(self):
        self.assertEqual(demjson.decode('{55:55}',strict=False), {55:55})
        self.assertEqual(demjson.decode('{fiftyfive:55}',strict=False), {'fiftyfive':55})
        self.assertRaises(demjson.JSONDecodeError, demjson.decode,
                          '{fiftyfive:55}', strict=True)
        self.assertRaises(demjson.JSONEncodeError, demjson.encode,
                          {55:'fiftyfive'}, strict=True)
        self.assertEqual(demjson.encode({55:55}, strict=False), '{55:55}')

    def testDecodeWhitespace(self):
        self.assertEqual(demjson.decode(' []'), [])
        self.assertEqual(demjson.decode('[] '), [])
        self.assertEqual(demjson.decode(' [ ] '), [])
        self.assertEqual(demjson.decode('\n[]\n'), [])
        self.assertEqual(demjson.decode('\t\r \n[\n\t]\n'), [])
        # Form-feed is not a valid JSON whitespace char
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, '\x0c[]', strict=True)
        # No-break-space is not a valid JSON whitespace char
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, u'\u00a0[]', strict=True)

    def testDecodeInvalidStartingType(self):
        if False:
            # THESE TESTS NO LONGER APPLY WITH RFC 7158, WHICH SUPERSEDED RFC 4627
            self.assertRaises(demjson.JSONDecodeError, demjson.decode, '', strict=True)
            self.assertRaises(demjson.JSONDecodeError, demjson.decode, '1', strict=True)
            self.assertRaises(demjson.JSONDecodeError, demjson.decode, '1.5', strict=True)
            self.assertRaises(demjson.JSONDecodeError, demjson.decode, '"a"', strict=True)
            self.assertRaises(demjson.JSONDecodeError, demjson.decode, 'true', strict=True)
            self.assertRaises(demjson.JSONDecodeError, demjson.decode, 'null', strict=True)

    def testDecodeMixed(self):
        self.assertEqual(demjson.decode('[0.5,{"3e6":[true,"d{["]}]'), \
                         [0.5, {'3e6': [True, 'd{[']}] )

    def testEncodeMixed(self):
        self.assertEqual(demjson.encode([0.5, {'3e6': [True, 'd{[']}] ),
                         '[0.5,{"3e6":[true,"d{["]}]' )

    def testDecodeComments(self):
        self.assertEqual(demjson.decode('//hi\n42', allow_comments=True), 42)
        self.assertEqual(demjson.decode('/*hi*/42', allow_comments=True), 42)
        self.assertEqual(demjson.decode('/*hi//x\n*/42', allow_comments=True), 42)
        self.assertEqual(demjson.decode('"a/*xx*/z"', allow_comments=True), 'a/*xx*/z')
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, \
                          '4/*aa*/2', allow_comments=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, \
                          '//hi/*x\n*/42', allow_comments=True)
        self.assertRaises(demjson.JSONDecodeError, demjson.decode, \
                          '/*hi/*x*/42', allow_comments=True)

    def testNamedTuples(self):
        import collections
        pt = collections.namedtuple('pt',['x','y'])
        a = pt(7,3)
        self.assertEqual(demjson.encode(a, encode_namedtuple_as_object=True, compactly=True),
                         '{"x":7,"y":3}' )
        self.assertEqual(demjson.encode(a, encode_namedtuple_as_object=False, compactly=True),
                         '[7,3]' )

    def testDecodeNumberHook(self):
        """Tests the 'decode_number' and 'decode_float' hooks."""
        def round_plus_one(s):
            return round(float(s)) + 1
        def negate(s):
            if s.startswith('-'):
                return float( s[1:] )
            else:
                return float( '-' + s )
        def xnonnum(s):
            if s=='NaN':
                return 'x-not-a-number'
            elif s=='Infinity' or s=='+Infinity':
                return 'x-infinity'
            elif s=='-Infinity':
                return 'x-neg-infinity'
            else:
                raise demjson.JSONSkipHook
        self.assertEqual(demjson.decode('[3.14,-2.7]'),
                         [3.14, -2.7] )
        self.assertEqual(demjson.decode('[3.14,-2.7]',decode_number=negate),
                         [-3.14, 2.7] )
        self.assertEqual(demjson.decode('[3.14,-2.7]',decode_number=round_plus_one),
                         [4.0, -2.0] )
        self.assertEqual(demjson.decode('[3.14,-2.7,8]',decode_float=negate),
                         [-3.14, 2.7, 8] )
        self.assertEqual(demjson.decode('[3.14,-2.7,8]',decode_float=negate,decode_number=round_plus_one),
                         [-3.14, 2.7, 9.0] )
        self.assertEqual(demjson.decode('[2,3.14,NaN,Infinity,+Infinity,-Infinity]',
                                        strict=False, decode_number=xnonnum),
                         [2, 3.14, 'x-not-a-number', 'x-infinity', 'x-infinity', 'x-neg-infinity'] )

    def testDecodeArrayHook(self):
        def reverse(arr):
            return list(reversed(arr))
        self.assertEqual(demjson.decode('[3, 8, 9, [1, 3, 5]]'),
                         [3, 8, 9, [1, 3, 5]] )
        self.assertEqual(demjson.decode('[3, 8, 9, [1, 3, 5]]', decode_array=reverse),
                         [[5, 3, 1], 9, 8, 3] )
        self.assertEqual(demjson.decode('[3, 8, 9, [1, 3, 5]]', decode_array=sum),
                         29 )

    def testDecodeObjectHook(self):
        def pairs(dct):
            return sorted(dct.items())
        self.assertEqual(demjson.decode('{"a":42, "b":{"c":99}}'),
                         {u'a': 42, u'b': {u'c': 99}} )
        self.assertEqual(demjson.decode('{"a":42, "b":{"c":99}}', decode_object=pairs),
                         [(u'a', 42), (u'b', [(u'c', 99)])] )

    def testDecodeStringHook(self):
        import string
        def s2num( s ):
            try:
                s = int(s)
            except ValueError:
                pass
            return s
        doc = '{"one":["two","three",{"four":"005"}]}'
        self.assertEqual(demjson.decode(doc),
                         {'one':['two','three',{'four':'005'}]} )
        self.assertEqual(demjson.decode(doc, decode_string=lambda s: s.capitalize()),
                         {'One':['Two','Three',{'Four':'005'}]} )
        self.assertEqual(demjson.decode(doc, decode_string=s2num),
                         {'one':['two','three',{'four':5}]} )


    def testEncodeDictKey(self):
        d1 = {42: "forty-two", "a":"Alpha"}
        d2 = {complex(0,42): "imaginary-forty-two", "a":"Alpha"}

        def make_key( k ):
            if isinstance(k,basestring):
                raise demjson.JSONSkipHook
            else:
                return repr(k)

        def make_key2( k ):
            if isinstance(k, (int,basestring)):
                raise demjson.JSONSkipHook
            else:
                return repr(k)

        self.assertRaises(demjson.JSONEncodeError, demjson.encode, \
                          d1, strict=True)
        self.assertEqual(demjson.encode(d1,strict=False),
                         '{"a":"Alpha",42:"forty-two"}' )

        self.assertEqual(demjson.encode(d1, encode_dict_key=make_key),
                         '{"42":"forty-two","a":"Alpha"}' )
        self.assertEqual(demjson.encode(d1,strict=False, encode_dict_key=make_key2),
                         '{"a":"Alpha",42:"forty-two"}' )

        self.assertRaises(demjson.JSONEncodeError, demjson.encode, \
                          d2, strict=True)
        self.assertEqual(demjson.encode(d2, encode_dict_key=make_key),
                         '{"%r":"imaginary-forty-two","a":"Alpha"}' % complex(0,42) )

    def testEncodeDict(self):
        def d2pairs( d ):
            return sorted( d.items() )
        def add_keys( d ):
            d['keys'] = list(sorted(d.keys()))
            return d

        d = {"a":42, "b":{"c":99,"d":7}}
        self.assertEqual(demjson.encode( d, encode_dict=d2pairs ),
                         '[["a",42],["b",[["c",99],["d",7]]]]' )
        self.assertEqual(demjson.encode( d, encode_dict=add_keys ),
                         '{"a":42,"b":{"c":99,"d":7,"keys":["c","d"]},"keys":["a","b"]}' )

    def testEncodeSequence(self):
        def list2hash( seq ):
            return dict(enumerate(seq))
        d = [1,2,3,[4,5,6],7,8]
        self.assertEqual(demjson.encode( d, encode_sequence=reversed ),
                         '[8,7,[6,5,4],3,2,1]' )
        self.assertEqual(demjson.encode( d, encode_sequence=list2hash ),
                         '{0:1,1:2,2:3,3:{0:4,1:5,2:6},4:7,5:8}' )

    @skipUnlessPython3
    def testEncodeBytes(self):
        no_bytes = bytes([])
        all_bytes = bytes( list(range(256)) )

        self.assertEqual(demjson.encode( no_bytes ),
                         '[]' )
        self.assertEqual(demjson.encode( all_bytes ),
                         '[' + ','.join([str(n) for n in all_bytes]) + ']' )

        self.assertEqual(demjson.encode( no_bytes, encode_bytes=hexencode_bytes ),
                         '""' )
        self.assertEqual(demjson.encode( all_bytes, encode_bytes=hexencode_bytes ),
                         '"' + hexencode_bytes(all_bytes) + '"' )


    def testEncodeValue(self):
        def enc_val( val ):
            if isinstance(val, complex):
                return {'real':val.real, 'imaginary':val.imag}
            elif isinstance(val, basestring):
                return val.upper()
            elif isinstance(val, datetime.date):
                return val.strftime("Year %Y Month %m Day %d")
            else:
                raise demjson.JSONSkipHook

        v = {'ten':10, 'number': complex(3, 7.1), 'asof': datetime.date(2014,1,17)}
        self.assertEqual(demjson.encode( v, encode_value=enc_val ),
                         u'{"ASOF":"YEAR 2014 MONTH 01 DAY 17","NUMBER":{"IMAGINARY":7.1,"REAL":3.0},"TEN":10}' )

    def testEncodeDefault(self):
        import datetime
        def dictkeys( d ):
            return "/".join( sorted([ str(k) for k in d.keys() ]) )
        def magic( d ):
            return complex( 1, len(d))

        vals = [ "abc", 123, datetime.date(2014,1,17), sys, {'a':42,'wow':True} ]

        self.assertEqual(demjson.encode( vals, encode_default=repr ),
                         u'["abc",123,"%s","%s",{"a":42,"wow":true}]' % ( repr(vals[2]), repr(vals[3])) )

        self.assertEqual(demjson.encode( vals, encode_default=repr, encode_dict=dictkeys ),
                         u'["abc",123,"%s","%s","a/wow"]' % ( repr(vals[2]), repr(vals[3])) )

        self.assertEqual(demjson.encode( vals, encode_default=repr, encode_dict=magic ),
                         u'["abc",123,"%s","%s","%s"]' % ( repr(vals[2]), repr(vals[3]), repr(magic(vals[4])) ) )


    def testEncodeDefaultMethod(self):
        class Anon(object):
            def __init__(self, val):
                self.v = val

        class MyJSON(demjson.JSON):
            def encode_default(self, obj, nest_level=0 ):
                if isinstance(obj,Anon):
                    return obj.v
                raise demjson.JSONEncodeError("Default case not handled")

        def check_orig(v):
            j = demjson.JSON()
            return j.encode(v)

        self.assertRaises( demjson.JSONEncodeError, check_orig, Anon("Hello") )

        myj = MyJSON()
        self.assertEqual( myj.encode( Anon("Hello") ), '"Hello"' )


def run_all_tests():
    print 'Running with demjson version', demjson.__version__
    unittest.main()
    
if __name__ == '__main__':
    run_all_tests()

# end file

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module tests demjson.py using unittest.

"""

import sys, os, time
import unittest

# Force PYTHONPATH to head of sys.path, as the easy_install (egg files) will
# have rudely forced itself ahead of PYTHONPATH.

for pos, name in enumerate(os.environ.get('PYTHONPATH','').split(os.pathsep)):
    if os.path.isdir(name):
        sys.path.insert(pos, name)

import demjson

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

    def testDecodeStringRawUnicode(self):
        self.assertEqual(demjson.decode('"\xc3\xa0"', encoding='utf-8'), u'\u00e0')

        self.assertEqual(demjson.decode('"\x00\x00\x00\xe0\x00\x00\x00"\x00\x00\x00',
                                        encoding='ucs4le'), u'\u00e0')
        self.assertEqual(demjson.decode('\x00\x00\x00"\x00\x00\x00\xe0\x00\x00\x00"',
                                        encoding='ucs4be'), u'\u00e0')
        self.assertEqual(demjson.decode('\x00\x00\x00"\x00\x00\x00\xe0\x00\x00\x00"',
                                        encoding='utf-32be'), u'\u00e0')
        self.assertEqual(demjson.decode('\x00\x00\xfe\xff\x00\x00\x00"\x00\x00\x00\xe0\x00\x00\x00"',
                                        encoding='ucs4'), u'\u00e0')

    def testEncodeStringRawUnicode(self):
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='utf-8'),
                         '"\xc3\xa0"')
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='ucs4le'),
                         '"\x00\x00\x00\xe0\x00\x00\x00"\x00\x00\x00')
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='ucs4be'),
                         '\x00\x00\x00"\x00\x00\x00\xe0\x00\x00\x00"')
        self.assertEqual(demjson.encode(u'\u00e0', escape_unicode=False, encoding='utf-32be'),
                         '\x00\x00\x00"\x00\x00\x00\xe0\x00\x00\x00"')
        self.assert_(demjson.encode(u'\u00e0', escape_unicode=False, encoding='ucs4')
                     in ['\x00\x00\xfe\xff\x00\x00\x00"\x00\x00\x00\xe0\x00\x00\x00"',
                         '\xff\xfe\x00\x00"\x00\x00\x00\xe0\x00\x00\x00"\x00\x00\x00'] )

    def testDecodeSupplementalUnicode(self):
        import sys
        if sys.maxunicode > 65535:
            self.assertEqual(demjson.decode(r'"\udbc8\udf45"'), u'\U00102345')
            self.assertEqual(demjson.decode(r'"\ud800\udc00"'), u'\U00010000')
            self.assertEqual(demjson.decode(r'"\udbff\udfff"'), u'\U0010ffff')
        for bad_case in [r'"\ud801"', r'"\udc02"',
                         r'"\ud801\udbff"', r'"\ud801\ue000"',
                         r'"\ud801\u2345"']:
            try:
                self.assertRaises(demjson.JSONDecodeError, demjson.decode(bad_case))
            except demjson.JSONDecodeError:
                pass

    def testEncodeSupplementalUnicode(self):
        import sys
        if sys.maxunicode > 65535:
            self.assertEqual(demjson.encode(u'\U00010000'), r'"\ud800\udc00"')
            self.assertEqual(demjson.encode(u'\U00102345'), r'"\udbc8\udf45"')
            self.assertEqual(demjson.encode(u'\U0010ffff'), r'"\udbff\udfff"')

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
        import UserDict
        import string
        class LikeDict(UserDict.DictMixin):
            def __getitem__(self,key):
                import string
                if key in string.ascii_uppercase:
                    return ord(key)
                raise KeyError('No such key', key)
            def __setitem__(self,key): raise RuntimeError('read only object')
            def __delitem__(self,key): raise RuntimeError('read only object')
            def keys(self):
                import string
                return list(string.ascii_uppercase)
        mydict = LikeDict()
        self.assertEqual(demjson.encode(mydict), \
                         '{' + ','.join(['"%s":%d'%(c,ord(c)) for c in string.ascii_uppercase]) + '}' )

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
        self.assertEqual(demjson.encode(mystring, escape_unicode=True, encoding='utf-8'), r'"hi\u2012there"')

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

def run_all_tests():
    print 'Running with demjson version', demjson.__version__
    unittest.main()
    
if __name__ == '__main__':
    run_all_tests()

# end file

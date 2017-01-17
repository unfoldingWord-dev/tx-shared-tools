from __future__ import unicode_literals
import unittest
from general_tools.string_utils import try_parse_int


class StringUtilsTest(unittest.TestCase):

    def test_try_parse_int(self):

        # test positive, negative and zero integer strings
        success, int_val = try_parse_int('123')
        self.assertTrue(success)
        self.assertEqual(123, int_val)
        self.assertIsInstance(int_val, int)

        success, int_val = try_parse_int('-123')
        self.assertTrue(success)
        self.assertEqual(-123, int_val)
        self.assertIsInstance(int_val, int)

        success, int_val = try_parse_int('0')
        self.assertTrue(success)
        self.assertEqual(0, int_val)
        self.assertIsInstance(int_val, int)

        # test actual int values
        # noinspection PyTypeChecker
        success, int_val = try_parse_int(123)
        self.assertTrue(success)
        self.assertEqual(123, int_val)
        self.assertIsInstance(int_val, int)

        # test decimals
        success, int_val = try_parse_int('1.23')
        self.assertFalse(success)
        self.assertIsNone(int_val)

        # test strings containing some digits also
        success, int_val = try_parse_int('1a2b3')
        self.assertFalse(success)
        self.assertIsNone(int_val)

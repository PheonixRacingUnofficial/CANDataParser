import unittest
from fpu_can_parser.parser.hex_helper import (
    hex_to_int8, hex_to_uint8, hex_to_int16, hex_to_uint16,
    hex_to_int32, hex_to_uint32, hex_to_float, hex_to_bits, hex_inverter
)

class TestHexHelper(unittest.TestCase):

    def test_hex_inverter(self):
        self.assertEqual(hex_inverter("1234"), "3412")
        self.assertEqual(hex_inverter("AABBCCDD"), "DDCCBBAA")

    def test_hex_to_int8(self):
        self.assertEqual(hex_to_int8("FF"), -1)
        self.assertEqual(hex_to_int8("80"), -128)
        self.assertEqual(hex_to_int8("7F"), 127)

    def test_hex_to_uint8(self):
        self.assertEqual(hex_to_uint8("FF"), 255)
        self.assertEqual(hex_to_uint8("00"), 0)

    def test_hex_to_int16(self):
        self.assertEqual(hex_to_int16("FFFE"), -257)
        self.assertEqual(hex_to_int16("8000"), 128)
        self.assertEqual(hex_to_int16("7FFF"), -129)

    def test_hex_to_uint16(self):
        self.assertEqual(hex_to_uint16("FFFF"), 65535)
        self.assertEqual(hex_to_uint16("FF00"), 255)

    def test_hex_to_int32(self):
        self.assertEqual(hex_to_int32("FFFFFFFF"), -1)
        self.assertEqual(hex_to_int32("80000000"), 128)
        self.assertEqual(hex_to_int32("7FFFFFFF"), -129)

    def test_hex_to_uint32(self):
        self.assertEqual(hex_to_uint32("FFFFFFFF"), 4294967295)
        self.assertEqual(hex_to_uint32("00000001"), 16777216)

    def test_hex_to_float(self):
        self.assertAlmostEqual(hex_to_float("0000803F"), 1.0)    # 0x3F800000 = 1.0
        self.assertAlmostEqual(hex_to_float("000080BF"), -1.0)   # 0xBF800000 = -1.0
        self.assertAlmostEqual(hex_to_float("00000000"), 0.0)

    def test_hex_to_bits(self):
        self.assertEqual(hex_to_bits("0F"), "00001111")
        self.assertEqual(hex_to_bits("1F"), "00011111")
        self.assertEqual(hex_to_bits("FF"), "11111111")

        self.assertEqual(hex_to_bits("0000"), "0000000000000000")
        self.assertEqual(hex_to_bits("00FF"), "1111111100000000")
        self.assertEqual(hex_to_bits("FF00"), "0000000011111111")

if __name__ == "__main__":
    unittest.main()

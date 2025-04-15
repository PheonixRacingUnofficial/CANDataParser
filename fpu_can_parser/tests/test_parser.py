import io
import unittest
from unittest.mock import patch

from fpu_can_parser.parser import parser, sensor, sensor_manager

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = parser.Parser("./test_files/test_sensor_file.txt", debug=False, log=False)
        self.sensor_manager = sensor_manager.SensorManager("./test_files/test_sensor_file.txt")
        self.sensor = sensor.Sensor(0x300, "bmuhbs", "%ui32%ui32", "%hbid%hbsn")

    def test_parser(self):
        # Test with a valid CAN line
        data = "(1727120880.730751) can0 300#05500000AB0D0000"
        expected_output =  ('2024-09-23 15:48:00.730751', '0x300', {'hbid': 20485, 'hbsn': 3499})
        result = self.parser.parse_can_line(data)
        self.assertEqual(result, expected_output)

        # Test with a valid PCAN line
        data = "Timestamp: 1727730784.466013    ID:      300    S Rx                DL:  8    05 50 00 00 ab 0d 00 00     Channel: can0"
        expected_output = ('2024-09-30 17:13:04.466013', '0x300', {'hbid': 20485, 'hbsn': 3499})
        result = self.parser.parse_can_line(data)
        self.assertEqual(result, expected_output)

        # Test with a valid TRC line
        data = "    30)       331.7  Rx         0300  8  05 50 00 00 AB 0D 00 00"
        expected_output = ('1969-12-31 19:00:00', '0x300', {'hbid': 20485, 'hbsn': 3499})
        result = self.parser.parse_can_line(data)
        self.assertEqual(result, expected_output)

        # Test with an invalid CAN line
        data = "Invalid CAN line"
        with self.assertRaises(ValueError):
            self.parser.parse_can_line(data)

    def test_sensor_manager(self):
        # Test with a valid CAN line
        data = "05500000AB0D0000"
        expected_output = {'hbid': 20485, 'hbsn': 3499}
        result = self.sensor_manager.pass_to_sensor(0x300, data)
        self.assertEqual(result, expected_output)

        # Test with an invalid CAN line
        data = "Invalid Sensor ID"
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.sensor_manager.pass_to_sensor(0x301, data)
            self.assertIn("WARNING: Sensor ID not found in loaded sensors", fake_out.getvalue().strip())

    def test_sensor(self):
        # Test with a valid data format
        data = "05500000AB0D0000"
        expected_output = {'hbid': 20485, 'hbsn': 3499}
        result = self.sensor.parse_data(data)
        self.assertEqual(result, expected_output)

        # Test with an invalid data format
        data = "Invalid Data Format"
        with self.assertRaises(ValueError):
            self.sensor.parse_data(data)



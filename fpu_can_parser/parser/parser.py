import datetime
import re
from typing import Dict, Tuple

from fpu_can_parser.parser.logger import Logger
from fpu_can_parser.parser.sensor_manager import SensorManager

class Parser:

    """
    This class is responsible for parsing CAN data lines and converting them into a more readable format.
    It handles different formats of CAN data, including standard CAN, TRC log data, and PCAN log data.
    """

    sensor_manager: SensorManager
    console: Logger
    trc_timestamp: datetime

    def __init__(self, sensor_file: str, debug: bool = False, log: bool = False, ):
        self.sensor_manager = SensorManager(sensor_file)
        self.console = Logger(debug, log)
        self.trc_timestamp = datetime.datetime.fromtimestamp(float('0000000000.000000'))


    def parse_can_line(self, data: str) -> Tuple[str, str, Dict[str, str]] | None:

        if data[0] == ';':
            # TRC Header Data, should not be parsed only used for the timestamp
            self.console.debug("This is a trc data header line")
            if data.__contains__('TIMESTAMP'):
                self.trc_timestamp += datetime.datetime.fromtimestamp(float(data.split('TIMESTAMP')[1]))

            return

        data = translate_can_format(data)

        timestamp = re.findall(r'\(([^)]+)\)', data)[0]
        data: str = data.split(' ')[2]
        sensor_id: str = hex(int(data[:3], 16))
        sensor_id_int: int = int(sensor_id, 16)
        sensor_data: str = data.split('#')[1]
        self.console.debug(
            [f"Data: {data}",
             f"Timestamp: {timestamp}",
             f"Sensor ID: {sensor_id}",
             f"Sensor ID (int): {sensor_id_int}"]
        )

        readable_time = f'{str(datetime.datetime.fromtimestamp(float(timestamp)))}'

        return readable_time, sensor_id, self.sensor_manager.pass_to_sensor(sensor_id_int, sensor_data)

def translate_can_format(data: str) -> str:
    if data[0] == '(':
        # Normal CAN data
        return data

    if bool(re.search(r'\d+\)', data)):
        # TRC Log Data
        can = "(0000000000.000000) can0 "
        data = data[33:]
        can += data[:3] + '#' + data[6:].replace(' ', '')
        return can

    if data.startswith('Timestamp'):
        # PCAN Log Data
        can = f"({data.split('Timestamp')[1].split(' ')[1]}) can0 "
        sensor = data.split('ID:')[1][:9].replace(' ', '')
        data = data.split('DL:  8')[1][:102 - 75].replace(' ', '')
        can += sensor + '#' + data
        return can

    raise ValueError(f"Unsupported data format; line: {data}")

def test_import():
    """
    This function is used to test the import of the Parser class.
    It creates an instance of the Parser class and prints the sensor manager.
    """
    print("Testing import of Parser class")





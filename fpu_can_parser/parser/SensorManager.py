import os
import re
from typing import Dict
from fpu_can_parser.parser.Sensor import Sensor

class SensorManager:

    loaded_sensors = Dict[int, Sensor]

    def __init__(self, sensor_file: str):
        self.loaded_sensors = get_sensors_from_file(os.path.abspath(sensor_file))

    def pass_to_sensor(self, sensor_id: int, data: str) -> Dict[str, str]:
        """
        This function passes the data to the sensor and returns the parsed data.

        :param sensor_id: Sensor ID
        :param data: Data to be parsed
        :return: Parsed data
        :rtype: Dict[str, str]
        """
        if sensor_id not in self.loaded_sensors:
            print("WARNING: Sensor ID not found in loaded sensors")
            return {str(sensor_id): "No Sensor Found"}
            # raise ValueError(f"Sensor with ID {sensor_id} not found")

        sensor = self.loaded_sensors[sensor_id]
        return sensor.parse_data(data)


def get_sensors_from_file(sensor_file) -> Dict[int, Sensor]:
    """
    This function reads a sensor file and returns a dictionary of Sensor objects.
    The keys are the sensor IDs and the values are the Sensor objects.

    :param sensor_file: Path to the sensor file
    :return: Dictionary of Sensor objects
    :rtype: Dict[int, Sensor]
    :raises FileNotFoundError: If the sensor file does not exist

    Sensors must be defined as stated in the SensorManager.md file
    sensor_name_code will be defined in the SensorAlias.md file
    sensor_data_format will be defined in the SensorManager.md file
    sensor_data_description_code will be defined in the SensorAlias.md file
    Format: <sensor_id>,<sensor_name_code>,<sensor_data_format>,<sensor_data_description_code>
    Ex: 0x300,bmuhbs,%ui32%ui32,%hbid%hbsn

    """

    sensors = {}


    if not os.path.exists(sensor_file):
        raise FileNotFoundError(f"The file {sensor_file} does not exist")

    with open(sensor_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(',')
            if len(parts) != 4:
                raise ValueError(f"Invalid sensor definition, not enough arguments: {line}")

            verify_sensor(parts[0], parts[2], parts[3])

            sensor_id = int(parts[0], 16)
            sensor_name_code = parts[1]
            sensor_data_format_code = parts[2]
            sensor_data_description_code = parts[3]

            sensors[sensor_id] = Sensor(sensor_id, sensor_name_code, sensor_data_format_code, sensor_data_description_code)

    return sensors


def verify_sensor(sensor_id, sensor_data_format_code, sensor_data_description_code):
    """
    This function verifies the sensor definition.

    :param sensor_id: Sensor ID
    :param sensor_data_format: Sensor data format
    :param sensor_data_description_code: Sensor data description code

    :raises ValueError: If the sensor definition is invalid
    """

    # Ensure sensor data format and description code have the same number of parts
    sensor_data_format_parts = sensor_data_format_code.split('%')
    sensor_data_description_code_parts = sensor_data_description_code.split('%')
    if len(sensor_data_format_parts) != len(sensor_data_description_code_parts):
        raise ValueError(f"Invalid sensor definition, data format and description code length do not match: {sensor_id}")

    # Ensure the numbers sensor data format add up to 64
    total_bits = 0
    for part in sensor_data_format_parts:
        if part:
            try:
                total_bits += int(re.findall(r"\d+", part)[0])
            except ValueError:
                raise ValueError(f"Invalid sensor definition, invalid data format: {sensor_id}")


    if total_bits != 64:
        raise ValueError(f"Invalid sensor definition, data format does not add up to 64 bits: {sensor_id}")

if __name__ == "__main__":
    # Example usage
    input_path = input("Enter file path: ")
    sensor_manager = SensorManager(input_path)
    print(sensor_manager.pass_to_sensor(0x300, "05500000AB0D0000"))
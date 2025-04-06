import re
from typing import Dict, List, Any

import fpu_can_parser.parser.hex_helper as hh

# Length is equal to the number of bytes divided by 4
data_format_code_dict: Dict[str, callable] = {
    "ui8": hh.hex_to_uint8,
    "i8": hh.hex_to_int8,
    "ui16": hh.hex_to_uint16,
    "i16": hh.hex_to_int16,
    "ui32": hh.hex_to_uint32,
    "i32": hh.hex_to_int32,
    "f32": hh.hex_to_float,
    "b8": hh.hex_to_bits,
    "b16": hh.hex_to_bits,
    "b32": hh.hex_to_bits,
    "b64": hh.hex_to_bits,
    "g8": 2,
    "g16": 4,
    "g32": 8,
    "g64": 16,
    # Add more data format codes as needed
}

class Sensor:
    """
    This class represents a sensor with its ID, name code, data format, and description code.
    It also provides methods to get the sensor's data format and description code.
    """
    sensor_id: int
    sensor_name_code: str
    sensor_data_format_code: str
    sensor_data_description_code: str

    sensor_data_format: List[str]
    sensor_data_description: List[str]

    def __init__(self, sensor_id, sensor_name_code, sensor_data_format_code, sensor_data_description_code):
        self.sensor_id = sensor_id
        self.sensor_name_code = sensor_name_code
        self.sensor_data_format_code = sensor_data_format_code
        self.sensor_data_description_code = sensor_data_description_code

        self.sensor_data_format = sensor_data_format_code.split('%')[1:]
        self.sensor_data_description = sensor_data_description_code.split('%')[1:]

    def parse_data(self, data: str) -> Dict[str, str]:
        """
        This function parses the sensor data format and description code.
        It returns a dictionary of parsed data.
        """
        parsed_data: Dict[str, Any] = {}
        input_data_pos_initial: int = 0
        data_sections: List[str] = []
        # Using the data format code, the input str needs to be split up into the correct number of bytes
        for i in range(len(self.sensor_data_format)):
            input_data_pos_final = int(int(re.findall(r"\d+", self.sensor_data_format[i])[0]) / 4)
            data_sections.append(data[input_data_pos_initial:input_data_pos_final])
            data = data[input_data_pos_final:]

        for i in range(len(data_sections)):
            if self.sensor_data_format[i] in data_format_code_dict:
                # Skip if garbage data
                if self.sensor_data_format[i].__contains__("g"):
                    continue
                parsed_data[self.sensor_data_description[i]] = data_format_code_dict[self.sensor_data_format[i]](data_sections[i])
            else:
                raise ValueError(f"Invalid sensor definition, invalid data format: {self.sensor_id}")

        return parsed_data


# Test Sensor class with heartbeat sensor data
if __name__ == "__main__":
    # Example usage
    sensor = Sensor(0x300, "bmuhbs", "%ui32%ui32", "%hbid%hbsn")
    data = "05500000AB0D0000"
    sensor.parse_data(data)

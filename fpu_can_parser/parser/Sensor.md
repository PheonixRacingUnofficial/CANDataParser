# Sensor Class Documentation

## Overview
This module defines the `Sensor` class, which represents a sensor with an ID, name code, data format, and description code. It also provides methods to parse sensor data based on its format and description.

## Data Format Codes
A dictionary `data_format_code_dict` maps sensor data format codes to corresponding conversion functions or byte length values:

| Format Code | Function/Value |
|------------|----------------|
| `ui8`  | `hh.hex_to_uint8`  |
| `i8`   | `hh.hex_to_int8`   |
| `ui16` | `hh.hex_to_uint16` |
| `i16`  | `hh.hex_to_int16`  |
| `ui32` | `hh.hex_to_uint32` |
| `i32`  | `hh.hex_to_int32`  |
| `f32`  | `hh.hex_to_float`  |
| `b8`   | `hh.hex_to_bits`   |
| `b16`  | `hh.hex_to_bits`   |
| `b32`  | `hh.hex_to_bits`   |
| `b64`  | `hh.hex_to_bits`   |
| `g8`   | `2`               |
| `g16`  | `4`               |
| `g32`  | `8`               |
| `g64`  | `16`              |

## Sensor Class
### Attributes:
- `sensor_id` (int): Unique identifier of the sensor.
- `sensor_name_code` (str): Code representing the sensor's name.
- `sensor_data_format_code` (str): Format code defining the data structure.
- `sensor_data_description_code` (str): Description code providing meaning to data.
- `sensor_data_format` (List[str]): Parsed list of data formats.
- `sensor_data_description` (List[str]): Parsed list of data descriptions.

### Methods:
#### `__init__(self, sensor_id, sensor_name_code, sensor_data_format_code, sensor_data_description_code)`
Initializes a sensor object with the provided attributes.

#### `parse_data(self, data: str) -> Dict[str, str]`
Parses raw sensor data into a dictionary based on its format and description.

**Parameters:**
- `data` (str): Hexadecimal string of sensor data.

**Returns:**
- `Dict[str, str]`: Dictionary mapping descriptions to parsed values.

**Raises:**
- `ValueError`: If an invalid data format is encountered.

### Example Usage:
```python
if __name__ == "__main__":
    sensor = Sensor(0x300, "bmuhbs", "%ui32%ui32", "%hbid%hbsn")
    data = "05500000AB0D0000"
    parsed_output = sensor.parse_data(data)
    print(parsed_output)
```

## Error Handling
- If an invalid sensor data format is encountered, a `ValueError` is raised.
- The script ensures that data format codes align with the expected description codes.

## Notes
- Garbage data (`g8`, `g16`, `g32`, `g64`) is ignored during parsing.
- The script splits input data according to format lengths before conversion.
- `data_format_code_dict` can be extended to support additional formats.


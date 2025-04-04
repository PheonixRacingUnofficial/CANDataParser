# SensorManager

## Overview
`SensorManager` is a Python module designed to manage sensor data by loading sensor definitions from a file, parsing received data, and verifying sensor configurations. It utilizes a `Sensor` class to interpret incoming data based on predefined formats.

## Features
- Reads and loads sensor definitions from a file.
- Stores sensors in a dictionary, mapping sensor IDs to `Sensor` objects.
- Provides a method to pass raw sensor data to the appropriate `Sensor` for parsing.
- Validates sensor definitions to ensure correct formatting and data structure.

## File Format
The sensor file must follow the specified format:

```
<sensor_id>,<sensor_name_code>,<sensor_data_format>,<sensor_data_description_code>
```

Example:
```
0x300,bmuhbs,%ui32%ui32,%hbid%hbsn
```

### Definitions:
- **sensor_id**: Unique hexadecimal identifier for the sensor.
- **sensor_name_code**: Short code representing the sensor name.
- **sensor_data_format**: Format specification of the sensor data.
- **sensor_data_description_code**: Codes describing the meaning of each data part.


## Usage
To use the `SensorManager`, run the script and provide the path to a valid sensor file:

```sh
python SensorManager.py
```

Alternatively, it can be imported and used programmatically:

```python
from SensorManager import SensorManager

sensor_manager = SensorManager("path/to/sensor_file.txt")
parsed_data = sensor_manager.pass_to_sensor(0x300, "05500000AB0D0000")
print(parsed_data)
```

## Functionality

### `SensorManager`
#### `__init__(sensor_file: str)`
- Initializes the `SensorManager` by loading sensor definitions from a file.

#### `pass_to_sensor(sensor_id: int, data: str) -> Dict[str, str]`
- Passes raw data to the appropriate `Sensor` for parsing.
- Returns a dictionary of parsed data.
- Logs a warning if the sensor ID is not found.

### `get_sensors_from_file(sensor_file: str) -> Dict[int, Sensor]`
- Reads the sensor file and constructs a dictionary of `Sensor` objects.
- Validates the sensor format.
- Raises `FileNotFoundError` if the file does not exist.

### `verify_sensor(sensor_id, sensor_data_format_code, sensor_data_description_code)`
- Ensures the sensor format and description lengths match.
- Validates that the total bit count of data formats sums to 64.
- Raises `ValueError` for incorrect definitions.

## Error Handling
- **FileNotFoundError**: Raised if the provided sensor file does not exist.
- **ValueError**: Raised for incorrectly formatted sensor definitions.
- **KeyError**: If attempting to access an undefined sensor.


